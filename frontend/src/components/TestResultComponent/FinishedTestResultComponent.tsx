import React from "react";
import { formatDuration } from "../../utils/dateUtils";
import DisplayLogComponent from "../DisplayLogComponent/DisplayLogComponent";
import styles from "./FinishedTestResultComponent.module.scss";
import InfoBox from "../InfoBox/InfoBox";
import InfoBoxElement from "../InfoBox/InfoBoxElement/InfoBoxElement";
import ImageComparison from "../ImageComparison/ImageComparison";
import { FailureMessageBox } from "./MessageBoxes/MessageBoxes";
import TestResultComparisonResult from "../TestResultComparisonResult/TestResultComparisonResult";
import UpdateReferenceImageButton from "./UpdateReferenceImageButton";
import {
  ComparisonMethod,
  TestResultDto,
} from "../../catoapimodels/catoapimodels";
import Spinner from "../Spinner/Spinner";
import { ExclamationTriangle } from "react-bootstrap-icons";

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
      {props.result.unifiedTestStatus === "FAILED"
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

function anyImageHasTranscodingError(result: TestResultDto) {
  if (
    result.imageOutput &&
    result.imageOutput.transcodingState === "UNABLE_TO_TRANSCODE"
  ) {
    return true;
  }
  if (
    result.referenceImage &&
    result.referenceImage.transcodingState === "UNABLE_TO_TRANSCODE"
  ) {
    return true;
  }
  if (
    result.diffImage &&
    result.diffImage.transcodingState === "UNABLE_TO_TRANSCODE"
  ) {
    return true;
  }
  return false;
}

function allAvailableImagesAreTranscoded(result: TestResultDto) {
  if (
    result.imageOutput &&
    result.imageOutput.transcodingState !== "TRANSCODED"
  ) {
    return false;
  }
  if (
    result.referenceImage &&
    result.referenceImage.transcodingState !== "TRANSCODED"
  ) {
    return false;
  }
  if (result.diffImage && result.diffImage.transcodingState !== "TRANSCODED") {
    return false;
  }
  return true;
}

function renderImages(result: TestResultDto): React.ReactNode {
  if (anyImageHasTranscodingError(result)) {
    return (
      <div className={"d-flex align-items-center mb-3"}>
        <ExclamationTriangle size={16} />
        <span className={"ml-2"}>Unable to transcode one or more images.</span>
      </div>
    );
  }
  if (allAvailableImagesAreTranscoded(result)) {
    return (
      <React.Fragment>
        <ImageComparison
          imageOutput={result.imageOutput}
          referenceImage={result.referenceImage}
          diffImage={result.diffImage}
          comparisonMethod={
            result.comparisonSettings?.method || ComparisonMethod.SSIM
          }
        />
      </React.Fragment>
    );
  }
  return (
    <div className={"d-flex align-items-center mb-3"}>
      <Spinner />
      <span className={"ml-2"}>Transcoding...</span>
    </div>
  );
}

export default FinishedTestResultComponent;
