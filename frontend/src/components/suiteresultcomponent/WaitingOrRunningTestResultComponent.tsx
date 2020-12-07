import React from "react";
import TestResult from "../../models/TestResult";
import { formatTime } from "../../utils";
import RenderingBucketIcon from "../icons/RenderingBucketIcon";

interface Props {
  result: TestResult;
}

function WaitingOrRunningTestResultComponent(props: Props) {
  return (
    <div>
      <p>
        {props.result.execution_status === "NOT_STARTED" ? (
          "waiting to start"
        ) : (
          <RenderingBucketIcon />
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
