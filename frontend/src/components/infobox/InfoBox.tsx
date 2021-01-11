import React from "react";
import styles from "../runsummary/RunSummary.module.scss";

interface Props {
  className?: string;
}

const InfoBox: React.FunctionComponent<Props> = (props) => {
  return (
    <div className={styles.runSummaryInfoBox + " " + props.className}>
      {props.children}
    </div>
  );
};

export default InfoBox;
