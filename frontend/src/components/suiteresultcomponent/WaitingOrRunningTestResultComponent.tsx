import React from "react";
import TestResult from "../../models/TestResult";
import { formatTime } from "../../utils";
import {GridLoader} from "react-spinners";

interface Props {
  result: TestResult;
}

function WaitingOrRunningTestResultComponent(props: Props) {
  return (
    <div>
      <p>
        {props.result.execution_status === "NOT_STARTED"
          ? "waiting to start"
          : <GridLoader size={5}/>}
      </p>
      <p>
        {props.result.started_at
          ? "started: " + formatTime(props.result.started_at)
          : ""}
      </p>
      <p>Command: "{props.result.test_command}"</p>
    </div>
  );
}

export default WaitingOrRunningTestResultComponent;
