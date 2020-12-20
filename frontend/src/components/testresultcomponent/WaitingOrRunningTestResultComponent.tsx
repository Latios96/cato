import React from "react";
import RenderingBucketIcon from "../icons/RenderingBucketIcon";
import { formatTime } from "../../utils";
import { TestResultDto } from "../../catoapimodels";

interface Props {
  result: TestResultDto;
}

function WaitingOrRunningTestResultComponent(props: Props) {
  return (
    <div>
      <p>
        {props.result.execution_status === "NOT_STARTED" ? (
          "waiting to start"
        ) : (
          <RenderingBucketIcon isActive={false} />
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
