from cato_server.domain.image import ImageChannel, Image
from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.output import Output
from cato_server.domain.project import Project
from cato_server.domain.run import Run
from cato_server.domain.suite_result import SuiteResult
from cato_server.domain.test_result import TestResult
from cato_server.mappers.image_channel_class_mapper import ImageChannelClassMapper
from cato_server.mappers.image_class_mapper import ImageClassMapper
from cato_server.mappers.machine_info_class_mapper import MachineInfoClassMapper
from cato_server.mappers.mapper_registry import MapperRegistry
from cato_server.mappers.output_class_mapper import OutputClassMapper
from cato_server.mappers.project_class_mapper import ProjectClassMapper
from cato_server.mappers.run_class_mapper import RunClassMapper
from cato_server.mappers.suite_result_class_mapper import SuiteResultClassMapper
from cato_server.mappers.test_result_class_mapper import TestResultClassMapper


class MapperRegistryFactory:
    def create_mapper_registry(self) -> MapperRegistry:
        mapper_registry = MapperRegistry()

        mapper_registry.register_mapper(Project, ProjectClassMapper())
        mapper_registry.register_mapper(ImageChannel, ImageChannelClassMapper())
        mapper_registry.register_mapper(Image, ImageClassMapper())
        mapper_registry.register_mapper(MachineInfo, MachineInfoClassMapper())
        mapper_registry.register_mapper(Output, OutputClassMapper())
        mapper_registry.register_mapper(Run, RunClassMapper())
        mapper_registry.register_mapper(SuiteResult, SuiteResultClassMapper())
        mapper_registry.register_mapper(TestResult, TestResultClassMapper())

        return mapper_registry
