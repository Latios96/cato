import React from "react";
import styles from "../runsummary/RunSummary.module.scss";
interface Props {
  value: string;
  title: string;
}
const InfoBoxElement = (props: Props) => {
  return (
    <div className={styles.infoBoxElement}>
      <span className={styles.runSummaryInfoBoxValue}>{props.value}</span>
      <span>{props.title}</span>
    </div>
  );
};

export default InfoBoxElement;
