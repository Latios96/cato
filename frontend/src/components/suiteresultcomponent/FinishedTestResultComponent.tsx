import React from "react";
import TestResult from "../../models/TestResult";
import { formatDuration, formatTime } from "../../utils";

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
      <p>
        {props.result.seconds != null
          ? "duration: " + formatDuration(props.result.seconds)
          : ""}
      </p>
      <p>status: {props.result.status}</p>
      {props.result.status === "FAILED"
        ? renderFailureInformation(props.result)
        : ""}
      {renderImages(props.result)}
    </div>
  );
}

function renderFailureInformation(result: TestResult): React.ReactNode {
  return (
    <div>
      <p>{"message: " + result.message}</p>
      <p>Command: "{result.test_command}"</p>
    </div>
  );
}

function renderImages(result: TestResult): React.ReactNode {
  return (
    <React.Fragment>
      {result.image_output ? (
        <img
          src={"/api/v1/files/" + result.image_output}
          alt={"image output"}
        />
      ) : (
        ""
      )}
    </React.Fragment>
  );
}

export default FinishedTestResultComponent;
