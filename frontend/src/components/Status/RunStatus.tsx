import React from "react";
import { Check2All, Hourglass } from "react-bootstrap-icons";
import RenderingBucketIcon from "../Icons/RenderingBucketIcon";
import { XCircleIcon } from "@primer/octicons-react";
import styles from "./StatusStyles.module.scss";

interface Props {
  status: string;
  isActive: boolean;
}

const RunStatus = (props: Props) => {
  if (props.status === "NOT_STARTED") {
    return (
      <span
        className="d-inline-block"
        data-toggle="tooltip"
        title="not started"
      >
        <Hourglass size={27} />
      </span>
    );
  } else if (props.status === "RUNNING") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="running">
        <RenderingBucketIcon isActive={props.isActive} />
      </span>
    );
  } else if (props.status === "SUCCESS") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="success">
        <Check2All color="green" size={27} />
      </span>
    );
  } else if (props.status === "FAILED") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="failed">
        <XCircleIcon size={27} className={styles.errorIcon} />
      </span>
    );
  }
  return <span />;
};

export default RunStatus;
