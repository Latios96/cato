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
      {props.result.unifiedTestStatus === "NOT_STARTED" ? (
        <NotStartedMessageBox />
      ) : (
        <IsRenderingMessageBox startedAt={props.result.startedAt} />
      )}
    </div>
  );
}

export default WaitingOrRunningTestResultComponent;
