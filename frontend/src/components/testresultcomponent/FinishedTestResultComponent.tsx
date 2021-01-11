import React from "react";
import { formatDuration, formatTime } from "../../utils";
import DisplayLogComponent from "../displaylogcomponent/DisplayLogComponent";
import MultiChannelImageComparison from "../imagecomparison/MultiChannelImageComparison";
import { TestResultDto } from "../../catoapimodels";
import styles from "./FinishedTestResultComponent.module.scss";
import InfoBox from "../infobox/InfoBox";
import InfoBoxElement from "../infobox/InfoBoxElement";
interface Props {
  result: TestResultDto;
}

function FinishedTestResultComponent(props: Props) {
  return (
    <div className={styles.finishedTestResultContainer}>
      <InfoBox>
        <InfoBoxElement
          value={formatTime(props.result.started_at)}
          title={"started"}
        />
        <InfoBoxElement
          value={formatTime(props.result.finished_at)}
          title={"finished"}
        />
        <InfoBoxElement
          value={formatDuration(props.result.seconds)}
          title={"duration"}
        />
      </InfoBox>
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
