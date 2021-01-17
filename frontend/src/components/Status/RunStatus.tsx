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
    return <Hourglass size={27} />;
  } else if (props.status === "RUNNING") {
    return <RenderingBucketIcon isActive={props.isActive} />;
  } else if (props.status === "SUCCESS") {
    return <Check2All color="green" size={27} />;
  } else if (props.status === "FAILED") {
    return <XCircleIcon size={27} className={styles.errorIcon} />;
  }
  return <span />;
};

export default RunStatus;
