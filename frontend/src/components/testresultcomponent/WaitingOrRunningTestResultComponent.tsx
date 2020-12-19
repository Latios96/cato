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
        {props.result.executionStatus === "NOT_STARTED" ? (
          "waiting to start"
        ) : (
          <RenderingBucketIcon isActive={false} />
        )}
      </p>
      <p>
        {props.result.startedAt
          ? "started: " + formatTime(props.result.startedAt)
          : ""}
      </p>
    </div>
  );
}

export default WaitingOrRunningTestResultComponent;
