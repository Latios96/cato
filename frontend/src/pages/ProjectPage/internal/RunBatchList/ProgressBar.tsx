import React from "react";
import styles from "./ProgressBar.module.scss";
import Tooltip from "../../../../components/Tooltip/Tooltip";
interface Props {
  progressPercentage: number;
}

function ProgressBar(props: Props) {
  return (
    <Tooltip
      tooltipText={`${props.progressPercentage.toFixed(2)}%`}
      tooltippedElement={
        <div className={styles.progressOuter}>
          <div
            className={styles.progressBar}
            style={{ width: `${props.progressPercentage}%` }}
          ></div>
        </div>
      }
    />
  );
}

export default ProgressBar;
