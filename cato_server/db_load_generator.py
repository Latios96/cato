import argparse
import datetime
import random
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Iterable

import pinject
from PIL import Image as PilImage, ImageDraw as PilImageDraw
from faker import Faker
from sqlalchemy import create_engine

import cato
import cato_server
import cato_server.server_logging
from cato.domain.test_status import TestStatus
from cato_server.configuration.app_configuration_reader import AppConfigurationReader
from cato_server.configuration.bindings_factory import BindingsFactory
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.image import Image, ImageChannel
from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.project import Project
from cato_server.domain.run import Run
from cato_server.domain.suite_result import SuiteResult
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import Base

logger = cato_server.server_logging.logger

MULTIPLIER = 1000

RUNS_PER_PROJECT = 12 * MULTIPLIER

SUITES_PER_RUN = 50

TESTS_PERS_SUITE = 15

fake = Faker()


class DbLoadGenerator:
    def __init__(
        self,
        project_repository: ProjectRepository,
        run_repository: RunRepository,
        suite_result_repository: SuiteResultRepository,
        image_repository: ImageRepository,
        file_storage: AbstractFileStorage,
        test_result_repository: TestResultRepository,
    ):
        self._project_repository = project_repository
        self._run_repository = run_repository
        self._suite_result_repository = suite_result_repository
        self._store_image = StoreImage(file_storage, image_repository)
        self._test_result_repository = test_result_repository
        self._file_storage = file_storage
        self._image_repository = image_repository
        self.alpha = None
        self.reference_image = None
        self.output_image = None

    def generate_load(self):
        project_names = ["V-Ray", "Arnold", "Renderman", "Manuka"]
        executor = ThreadPoolExecutor()
        for project_name in project_names:
            executor.submit(lambda: self._generate_project(project_name))

    def _generate_project(self, project_name):
        logger.info("Generating project %s", project_name)
        project = self._project_repository.save(Project(id=0, name=project_name))
        self._generate_runs(project)

    def _generate_runs(self, project):
        logger.info("Generating runs for project %s", project.name)
        runs = self._run_repository.insert_many(
            [
                Run(id=0, project_id=project.id, started_at=datetime.datetime.now())
                for x in range(RUNS_PER_PROJECT)
            ]
        )
        self._generate_suites(runs, project.name)

    def _generate_suites(self, runs: Iterable[Run], project_name):
        choices = [
            "alpha",
            "analytic",
            "parametric",
            "area",
            "light",
            "geo",
            "aovs",
            "archive",
            "assemblies",
            "backfaces",
            "modifiers",
            "basic",
            "clamp",
            "camera",
            "sss",
            "osl",
            "obj",
            "light sampling",
            "scope",
            "shadow-terminator",
        ]
        suites = []
        for i, run in enumerate(runs):
            for i in range(SUITES_PER_RUN):
                suite_name = f"{random.choice(choices)} {random.choice(choices)}"
                suites.append(
                    SuiteResult(
                        id=0, run_id=run.id, suite_name=suite_name, suite_variables={}
                    )
                )
        logger.info("Inserting %s suite results", len(suites))
        suites = self._suite_result_repository.insert_many(suites)
        logger.info("Inserted %s suite results", len(suites))
        self._generate_test_results(suites, project_name)

    def _generate_test_results(self, suites: Iterable[SuiteResult], project_name):
        total_count = len(suites) * TESTS_PERS_SUITE
        logger.info("Generating %s, test results..", total_count)
        test_names = [fake.name() for x in range(TESTS_PERS_SUITE)]

        results_to_save = []

        inserted = 0
        start = time.time()
        for suite in suites:
            for test_name in test_names:
                # todo generate output text
                reference_image = self._generate_reference_image(
                    project_name, suite.suite_name, test_name
                )
                output_image = self._generate_output_image(
                    project_name, suite.suite_name, test_name, "test"
                )

                test_result = TestResult(
                    id=0,
                    suite_result_id=suite.id,
                    test_name=test_name,
                    test_identifier=TestIdentifier(
                        suite_name=suite.suite_name, test_name=test_name
                    ),
                    test_command="my_command",
                    test_variables={},
                    machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
                    execution_status=ExecutionStatus.FINISHED,
                    status=TestStatus.SUCCESS,
                    seconds=fake.pyint(),
                    message="success",
                    image_output=output_image.id,
                    reference_image=reference_image.id,
                    started_at=datetime.datetime.now(),
                    finished_at=datetime.datetime.now(),
                )
                results_to_save.append(test_result)
                insert_count = len(results_to_save)
                if insert_count == 10000:
                    self._test_result_repository.insert_many(results_to_save)
                    stop = time.time()
                    inserted += insert_count
                    logger.info(
                        "Inserted %.2f percent of project test results in %.2fs",
                        float(inserted) / float(total_count) * 100,
                        stop - start,
                    )
                    results_to_save = []
                    start = time.time()

    def _generate_alpha(self):
        if not self.alpha:
            img = PilImage.new("RGB", (640, 480), color=(73, 109, 137))
            path = "alpha.png"
            img.save(path)
            self.alpha = self._file_storage.save_file(path)
        return self.alpha

    def _generate_reference_image(self, project_name, suite_name, test_name):
        if not self.reference_image:
            img = PilImage.new("RGB", (640, 480), color=(73, 109, 137))

            d = PilImageDraw.Draw(img)
            d.text(
                (100, 100),
                project_name + " " + suite_name + " " + test_name,
                fill=(255, 255, 0),
            )

            path = "reference_image.png"
            img.save(path)

            original_file = self._file_storage.save_file(path)
            self.reference_image = self._image_repository.save(
                Image(
                    id=0,
                    original_file_id=original_file.id,
                    channels=[
                        ImageChannel(
                            id=0, image_id=0, name="rgb", file_id=original_file.id
                        ),
                        ImageChannel(
                            id=0,
                            image_id=0,
                            name="alpha",
                            file_id=self._generate_alpha().id,
                        ),
                    ],
                    width=640,
                    height=480,
                    name="reference.png",
                )
            )
        return self.reference_image

    def _generate_output_image(self, project_name, suite_name, test_name, random):
        if not self.output_image:
            img = PilImage.new("RGB", (640, 480), color=(73, 109, 137))

            d = PilImageDraw.Draw(img)
            d.text(
                (100, 100),
                project_name + " " + suite_name + " " + test_name + " " + random,
                fill=(255, 255, 0),
            )
            # todo use tobytes? so we can keep this in memory?
            path = "output.png"
            img.save(path)

            original_file = self._file_storage.save_file(path)
            self.output_image = self._image_repository.save(
                Image(
                    id=0,
                    original_file_id=original_file.id,
                    channels=[
                        ImageChannel(
                            id=0, image_id=0, name="rgb", file_id=original_file.id
                        ),
                        ImageChannel(
                            id=0,
                            image_id=0,
                            name="alpha",
                            file_id=self._generate_alpha().id,
                        ),
                    ],
                    width=640,
                    height=480,
                    name=test_name,
                )
            )
        return self.output_image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="path to config.ini")
    args = parser.parse_args()

    path = get_config_path(args)
    config = AppConfigurationReader().read_file(path)

    engine = create_engine(config.storage_configuration.database_url)
    Base.metadata.create_all(engine)

    if config.logging_configuration.use_file_handler:
        cato_server.server_logging.setup_file_handler(
            "log.txt",
            config.logging_configuration.max_bytes,
            config.logging_configuration.backup_count,
        )

    bindings_factory: BindingsFactory = BindingsFactory(config)
    bindings = bindings_factory.create_bindings()

    obj_graph = pinject.new_object_graph(
        modules=[cato, cato_server], binding_specs=[bindings]
    )

    obj_graph.provide(DbLoadGenerator).generate_load()


def get_config_path(args):
    path = "config.ini"
    if args.config:
        path = args.config
    return path


if __name__ == "__main__":
    main()