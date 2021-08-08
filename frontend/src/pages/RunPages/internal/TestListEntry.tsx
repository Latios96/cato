import React from "react";
import {
  TestResultDto,
  TestResultShortSummaryDto,
} from "../../../catoapimodels";

interface Props {
  testResultDto: TestResultShortSummaryDto;
}

function TestListEntry(props: Props) {
  return (
    <tr>
      <td>{props.testResultDto.test_identifier.split("/")[0]}</td>
      <td>{props.testResultDto.test_identifier.split("/")[1]}</td>
    </tr>
  );
}

export default TestListEntry;
