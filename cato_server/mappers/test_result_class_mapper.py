from typing import Dict

from cato_server.domain.test_identifier import TestIdentifier
from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.mappers.datetime_value_mapper import DateTimeValueMapper
from cato_server.mappers.execution_status_value_mapper import ExecutionStatusValueMapper
from cato_server.mappers.machine_info_class_mapper import MachineInfoClassMapper
from cato_server.mappers.test_status_value_mapper import TestStatusValueMapper
from cato_server.domain.test_result import TestResult


class TestResultClassMapper(AbstractClassMapper):
    def __init__(self):
        self._date_time_value_mapper = DateTimeValueMapper()
        self._machine_info_class_mapper = MachineInfoClassMapper()
        self._execution_status_value_wrapper = ExecutionStatusValueMapper()
        self._test_status_value_wrapper = TestStatusValueMapper()

    def map_from_dict(self, the_dict: Dict) -> TestResult:
        return TestResult(
            id=the_dict.get("id") or 0,
            suite_result_id=the_dict["suite_result_id"],
            test_name=the_dict["test_name"],
            test_identifier=TestIdentifier.from_string(the_dict["test_identifier"]),
            test_command=the_dict["test_command"],
            test_variables=the_dict["test_variables"],
            machine_info=self._machine_info_class_mapper.map_from_dict(
                the_dict["machine_info"]
            ),
            execution_status=self._execution_status_value_wrapper.map_from(
                the_dict["execution_status"]
            ),
            status=self._test_status_value_wrapper.map_from(the_dict.get("status")),
            seconds=the_dict.get("seconds") or 0,
            message=the_dict.get("message"),
            image_output=the_dict.get("image_output"),
            reference_image=the_dict.get("reference_image"),
            started_at=self._date_time_value_mapper.map_from(
                the_dict.get("started_at")
            ),
            finished_at=self._date_time_value_mapper.map_from(
                the_dict.get("finished_at")
            ),
        )

    def map_to_dict(self, test_result: TestResult) -> Dict:
        data = {}

        self._map_required_attrs(test_result, data)
        self._map_optional_attrs(test_result, data)

        return data

    def _map_required_attrs(self, test_result, data):
        data["id"] = test_result.id
        data["suite_result_id"] = test_result.suite_result_id
        data["test_name"] = test_result.test_name
        data["test_identifier"] = str(test_result.test_identifier)
        data["test_command"] = test_result.test_command
        data["test_variables"] = test_result.test_variables
        data["machine_info"] = MachineInfoClassMapper().map_to_dict(
            test_result.machine_info
        )
        data["execution_status"] = test_result.execution_status.name

    def _map_optional_attrs(self, test_result, data):
        if test_result.status:
            data["status"] = test_result.status.name
        if test_result.seconds:
            data["seconds"] = test_result.seconds
        else:
            data["seconds"] = 0
        if test_result.message:
            data["message"] = test_result.message
        if test_result.image_output:
            data["image_output"] = test_result.image_output
        if test_result.reference_image:
            data["reference_image"] = test_result.reference_image
        if test_result.started_at:
            data["started_at"] = test_result.started_at.isoformat()
        if test_result.finished_at:
            data["finished_at"] = test_result.finished_at.isoformat()
