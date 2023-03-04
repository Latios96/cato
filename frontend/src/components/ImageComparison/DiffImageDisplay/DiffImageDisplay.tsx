import React from "react";
import styles from "./DiffImageDisplay.module.scss";
import SingleImageDisplay from "../SingleImageDisplay/SingleImageDisplay";
import { ComparisonMethod } from "../../../catoapimodels/catoapimodels";

interface Props {
  imageUrl: string;
  comparisonMethod: ComparisonMethod;
}

function DiffImageDisplay(props: Props) {
  return (
    <SingleImageDisplay imageUrl={props.imageUrl} informationText={"Diff"}>
      {props.comparisonMethod === ComparisonMethod.SSIM ? (
        <div className={styles.diffHighlightInformation}>
          <div style={{}} /> <span>Minimal Error</span>
          <div style={{}} /> <span>Maximal Error</span>
        </div>
      ) : null}
    </SingleImageDisplay>
  );
}

export default DiffImageDisplay;
