import React from "react";
import { TestResultDto } from "../../catoapimodels";
import {
  NotStartedMessageBox,
  IsRenderingMessageBox,
} from "./MessageBoxes/MessageBoxes";

interface Props {
  result: TestResultDto;
}

function WaitingOrRunningTestResultComponent(props: Props) {
  return (
    <div>
      {props.result.execution_status === "NOT_STARTED" ? (
        <NotStartedMessageBox />
      ) : (
        <IsRenderingMessageBox startedAt={props.result.started_at} />
      )}
    </div>
  );
}

export default WaitingOrRunningTestResultComponent;
