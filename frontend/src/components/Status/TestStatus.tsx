import React from "react";
import { Check, Hourglass } from "react-bootstrap-icons";
import RenderingBucketIcon from "../Icons/RenderingBucketIcon";
import { XCircleIcon } from "@primer/octicons-react";
import styles from "./StatusStyles.module.scss";

interface TestStatusData {
  execution_status: string;
  status: string | null | undefined;
}

interface Props {
  testResult: TestStatusData;
}
const TestStatus = (props: Props) => {
  if (props.testResult.execution_status === "NOT_STARTED") {
    return (
      <span
        className="d-inline-block"
        data-toggle="tooltip"
        title="not started"
      >
        <Hourglass size={27} />
      </span>
    );
  } else if (props.testResult.execution_status === "RUNNING") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="running">
        <RenderingBucketIcon isActive={false} />
      </span>
    );
  } else if (props.testResult.status === "SUCCESS") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="success">
        <Check color="green" size={27} />
      </span>
    );
  } else if (props.testResult.status === "FAILED") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="failed">
        <XCircleIcon size={27} className={styles.errorIcon} />
      </span>
    );
  }
  return <span />;
};

export default TestStatus;
