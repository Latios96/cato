import React from "react";
import { formatDuration, formatTime } from "../../utils";
import DisplayLogComponent from "../displaylogcomponent/DisplayLogComponent";
import MultiChannelImageComparison from "../imagecomparison/MultiChannelImageComparison";
import { TestResultDto } from "../../catoapimodels";

interface Props {
  result: TestResultDto;
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
        {props.result.seconds != null && props.result.seconds !== "NaN"
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

function renderFailureInformation(result: TestResultDto): React.ReactNode {
  return (
    <div>
      <p>{"message: " + result.message}</p>
      <p>Command: "{result.test_command}"</p>
    </div>
  );
}

function renderImages(result: TestResultDto): React.ReactNode {
  return (
    <React.Fragment>
      {result.image_output && result.reference_image ? (
        <MultiChannelImageComparison
          imageOutput={result.image_output}
          referenceImage={result.reference_image}
        />
      ) : (
        ""
      )}
    </React.Fragment>
  );
}

export default FinishedTestResultComponent;
