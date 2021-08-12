import React from "react";
import { SuiteResultDto } from "../../catoapimodels";
import { Check, Hourglass } from "react-bootstrap-icons";
import RenderingBucketIcon from "../Icons/RenderingBucketIcon";
import { XCircleIcon } from "@primer/octicons-react";
import styles from "./StatusStyles.module.scss";
interface Props {
  suiteResult: SuiteResultDto;
}

const SuiteStatus = (props: Props) => {
  if (props.suiteResult.status === "NOT_STARTED") {
    return (
      <span
        className="d-inline-block"
        data-toggle="tooltip"
        title="not started"
      >
        <Hourglass size={27} />
      </span>
    );
  } else if (props.suiteResult.status === "RUNNING") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="running">
        <RenderingBucketIcon isActive={false} />
      </span>
    );
  } else if (props.suiteResult.status === "SUCCESS") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="success">
        <Check color="green" size={27} />
      </span>
    );
  } else if (props.suiteResult.status === "FAILED") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="failed">
        <XCircleIcon size={27} className={styles.errorIcon} />
      </span>
    );
  }
  return <span />;
};

export default SuiteStatus;
