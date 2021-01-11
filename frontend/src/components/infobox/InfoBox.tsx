import React from "react";
import styles from "../runsummary/RunSummary.module.scss";

interface Props {}

const InfoBox: React.FunctionComponent<Props> = (props) => {
  return <div className={styles.runSummaryInfoBox}>{props.children}</div>;
};

export default InfoBox;
