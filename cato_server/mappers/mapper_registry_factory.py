from cato_server.domain.file import File
from cato_server.domain.image import ImageChannel, Image
from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.output import Output
from cato_server.domain.project import Project
from cato_server.domain.run import Run
from cato_server.domain.suite_result import SuiteResult
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.mappers.internal.file_class_mapper import FileClassMapper
from cato_server.mappers.internal.image_channel_class_mapper import (
    ImageChannelClassMapper,
)
from cato_server.mappers.internal.image_class_mapper import ImageClassMapper
from cato_server.mappers.internal.machine_info_class_mapper import (
    MachineInfoClassMapper,
)
from cato_server.mappers.internal.page_class_mapper import PageClassMapper
from cato_server.mappers.internal.test_identifier_class_mapper import (
    TestIdentifierClassMapper,
)
from cato_server.mappers.mapper_registry import MapperRegistry
from cato_server.mappers.internal.output_class_mapper import OutputClassMapper
from cato_server.mappers.internal.project_class_mapper import ProjectClassMapper
from cato_server.mappers.internal.run_class_mapper import RunClassMapper
from cato_server.mappers.internal.suite_result_class_mapper import (
    SuiteResultClassMapper,
)
from cato_server.mappers.internal.test_result_class_mapper import TestResultClassMapper
from cato_server.storage.abstract.page import Page


class MapperRegistryFactory:
    def create_mapper_registry(self) -> MapperRegistry:
        mapper_registry = MapperRegistry()

        mapper_registry.register_mapper(Project, ProjectClassMapper())
        mapper_registry.register_mapper(ImageChannel, ImageChannelClassMapper())
        mapper_registry.register_mapper(Image, ImageClassMapper())
        mapper_registry.register_mapper(File, FileClassMapper())
        mapper_registry.register_mapper(MachineInfo, MachineInfoClassMapper())
        mapper_registry.register_mapper(Output, OutputClassMapper())
        mapper_registry.register_mapper(Run, RunClassMapper())
        mapper_registry.register_mapper(SuiteResult, SuiteResultClassMapper())
        mapper_registry.register_mapper(TestResult, TestResultClassMapper())
        mapper_registry.register_mapper(TestIdentifier, TestIdentifierClassMapper())
        mapper_registry.register_mapper(Page, PageClassMapper(mapper_registry))

        return mapper_registry
