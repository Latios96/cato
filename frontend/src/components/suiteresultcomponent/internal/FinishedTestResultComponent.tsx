import React from "react";
import TestResult from "../../../models/TestResult";
import { formatDuration, formatTime } from "../../../utils";
import DisplayLogComponent from "../../displaylogcomponent/DisplayLogComponent";
import MultiChannelImageComparison from "../../imagecomparison/MultiChannelImageComparison";

interface Props {
  result: TestResult;
}

function FinishedTestResultComponent(props: Props) {
  return (
    <div>
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
      {props.result.status === "FAILED"
        ? renderFailureInformation(props.result)
        : ""}
      {renderImages(props.result)}
      <DisplayLogComponent testResultId={props.result.id} />
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
        <MultiChannelImageComparison
          imageOutputId={result.image_output}
          referenceImageId={result.reference_image ? result.reference_image : 0}
        />
      ) : (
        ""
      )}
    </React.Fragment>
  );
}

export default FinishedTestResultComponent;
