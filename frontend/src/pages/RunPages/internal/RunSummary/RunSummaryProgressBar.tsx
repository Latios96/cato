import { StatusPercentage } from "./utils";
import styles from "./RunSummary.module.scss";
import Tooltip from "../../../../components/Tooltip/Tooltip";
import React from "react";

export function RunSummaryProgressBar(props: {
  statusPercentage: StatusPercentage;
}) {
  return (
    <div className={styles.progressBar}>
      <Tooltip
        tooltipText={`${props.statusPercentage.succeeded.toFixed(
          2
        )}% succeeded`}
        tooltippedElement={
          <div
            style={{ width: `${props.statusPercentage.succeeded.toFixed(2)}%` }}
          />
        }
      />
      <Tooltip
        tooltipText={`${props.statusPercentage.failed.toFixed(2)}% failed`}
        tooltippedElement={
          <div
            style={{ width: `${props.statusPercentage.failed.toFixed(2)}%` }}
          />
        }
      />
      <Tooltip
        tooltipText={`${props.statusPercentage.running.toFixed(2)}% running`}
        tooltippedElement={
          <div
            style={{ width: `${props.statusPercentage.running.toFixed(2)}%` }}
          />
        }
      />
      <Tooltip
        tooltipText={`${props.statusPercentage.waitingToStart.toFixed(
          2
        )}% waiting to start`}
        tooltippedElement={
          <div
            style={{
              width: `${props.statusPercentage.waitingToStart.toFixed(2)}%`,
            }}
          />
        }
      />
    </div>
  );
}
