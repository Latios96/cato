import React from "react";
import { formatTime } from "../../utils";
import { TestResultDto } from "../../catoapimodels";
import InfoMessageBox from "../FailureMessageBox/InfoMessageBox";
import IsRenderingMessageBox from "../FailureMessageBox/IsRenderingMessageBox";

interface Props {
  result: TestResultDto;
}

function WaitingOrRunningTestResultComponent(props: Props) {
  return (
    <div>
      <p>
        {props.result.execution_status !== "NOT_STARTED" ? (
          <InfoMessageBox message={"waiting to start..."} />
        ) : (
          <IsRenderingMessageBox startedAt={props.result.started_at} />
        )}
      </p>
      <p>
        {props.result.started_at
          ? "started: " + formatTime(props.result.started_at)
          : ""}
      </p>
    </div>
  );
}

export default WaitingOrRunningTestResultComponent;
