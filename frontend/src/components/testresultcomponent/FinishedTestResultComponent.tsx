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
        {props.result.startedAt
          ? "started: " + formatTime(props.result.startedAt)
          : ""}
      </p>

      <p>
        {props.result.finishedAt
          ? "finished: " + formatTime(props.result.finishedAt)
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
      <p>Command: "{result.testCommand}"</p>
    </div>
  );
}

function renderImages(result: TestResultDto): React.ReactNode {
  return (
    <React.Fragment>
      {result.imageOutput && result.referenceImage ? (
        <MultiChannelImageComparison
          imageOutput={result.imageOutput}
          referenceImage={result.referenceImage}
        />
      ) : (
        ""
      )}
    </React.Fragment>
  );
}

export default FinishedTestResultComponent;
