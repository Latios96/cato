import React from "react";
import TestResult from "../../models/TestResult";
import { formatTime } from "../../utils";

interface Props {
  result: TestResult;
}

function FinishedTestResultComponent(props: Props) {
  return (
    <div>
      <p>Finished</p>
      <p>
        {props.result.started_at
          ? "started: " + formatTime(props.result.started_at)
          : ""}
      </p>
      <p>
        {props.result.finished_at
          ? "finished: " + formatTime(props.result.finished_at)
          : ""}
      </p>
      <p>duration: {props.result.seconds}</p>
      <p>status: {props.result.status}</p>
      {props.result.status === "FAILED"
        ? "message: " + props.result.message
        : ""}
      <p>Command: "{props.result.test_command}"</p>
      {props.result.image_output ? (
        <img src={"/api/v1/files/" + props.result.image_output} />
      ) : (
        ""
      )}
    </div>
  );
}

export default FinishedTestResultComponent;
