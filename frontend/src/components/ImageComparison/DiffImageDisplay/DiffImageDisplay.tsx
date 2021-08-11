import React from "react";
import styles from "./DiffImageDisplay.module.scss";
import SingleImageDisplay from "../SingleImageDisplay/SingleImageDisplay";

interface Props {
  imageUrl: string;
}

function DiffImageDisplay(props: Props) {
  return (
    <SingleImageDisplay imageUrl={props.imageUrl} informationText={"Diff"}>
      <div className={styles.diffHighlightInformation}>
        <div style={{}} /> <span>Minimal Error</span>
        <div style={{}} /> <span>Maximal Error</span>
      </div>
    </SingleImageDisplay>
  );
}

export default DiffImageDisplay;
