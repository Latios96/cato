import React from "react";
import { formatDuration } from "../../utils";
import DisplayLogComponent from "../DisplayLogComponent/DisplayLogComponent";
import { TestResultDto } from "../../catoapimodels";
import styles from "./FinishedTestResultComponent.module.scss";
import InfoBox from "../InfoBox/InfoBox";
import InfoBoxElement from "../InfoBox/InfoBoxElement/InfoBoxElement";
import FailureMessageBox from "../FailureMessageBox/FailureMessageBox";
import ImageComparison from "../ImageComparison/ImageComparison";
interface Props {
  result: TestResultDto;
}

function FinishedTestResultComponent(props: Props) {
  return (
    <div className={styles.finishedTestResultContainer}>
      <InfoBox className={styles.infoBox}>
        <InfoBoxElement
          id={"test-duration"}
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
  return <FailureMessageBox message={result.message} />;
}

function renderImages(result: TestResultDto): React.ReactNode {
  return (
    <React.Fragment>
      {result.image_output && result.reference_image ? (
        <ImageComparison
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
