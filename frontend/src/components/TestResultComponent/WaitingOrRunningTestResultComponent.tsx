import React from "react";
import {
  NotStartedMessageBox,
  IsRenderingMessageBox,
} from "./MessageBoxes/MessageBoxes";
import TestResultComparisonResult from "../TestResultComparisonResult/TestResultComparisonResult";
import { TestResultDto } from "../../catoapimodels/catoapimodels";

interface Props {
  result: TestResultDto;
}

function WaitingOrRunningTestResultComponent(props: Props) {
  return (
    <div>
      <TestResultComparisonResult testResult={props.result} />
      {props.result.unified_test_status === "NOT_STARTED" ? (
        <NotStartedMessageBox />
      ) : (
        <IsRenderingMessageBox startedAt={props.result.started_at} />
      )}
    </div>
  );
}

export default WaitingOrRunningTestResultComponent;
