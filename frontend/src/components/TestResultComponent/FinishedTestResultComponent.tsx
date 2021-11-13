import React from "react";
import { formatDuration } from "../../utils/dateUtils";
import DisplayLogComponent from "../DisplayLogComponent/DisplayLogComponent";
import { TestResultDto } from "../../catoapimodels";
import styles from "./FinishedTestResultComponent.module.scss";
import InfoBox from "../InfoBox/InfoBox";
import InfoBoxElement from "../InfoBox/InfoBoxElement/InfoBoxElement";
import ImageComparison from "../ImageComparison/ImageComparison";
import { FailureMessageBox } from "./MessageBoxes/MessageBoxes";
import TestResultComparisonResult from "../TestResultComparisonResult/TestResultComparisonResult";
import UpdateReferenceImageButton from "./UpdateReferenceImageButton";
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
      <TestResultComparisonResult testResult={props.result} />
      {props.result.unified_test_status === "FAILED"
        ? renderFailureInformation(props.result)
        : ""}
      {renderImages(props.result)}
      <UpdateReferenceImageButton testResultId={props.result.id} />
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
      <ImageComparison
        imageOutput={result.image_output}
        referenceImage={result.reference_image}
        diffImage={result.diff_image}
      />
    </React.Fragment>
  );
}

export default FinishedTestResultComponent;
