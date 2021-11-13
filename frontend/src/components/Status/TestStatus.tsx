import React from "react";
import { Check, Hourglass } from "react-bootstrap-icons";
import RenderingBucketIcon from "../Icons/RenderingBucketIcon";
import { XCircleIcon } from "@primer/octicons-react";
import styles from "./StatusStyles.module.scss";

interface TestStatusData {
  unified_test_status: string;
}

interface Props {
  testResult: TestStatusData;
}
const TestStatus = (props: Props) => {
  if (props.testResult.unified_test_status === "NOT_STARTED") {
    return (
      <span
        className="d-inline-block"
        data-toggle="tooltip"
        title="not started"
      >
        <Hourglass size={27} />
      </span>
    );
  } else if (props.testResult.unified_test_status === "RUNNING") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="running">
        <RenderingBucketIcon isActive={false} />
      </span>
    );
  } else if (props.testResult.unified_test_status === "SUCCESS") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="success">
        <Check color="green" size={27} />
      </span>
    );
  } else if (props.testResult.unified_test_status === "FAILED") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="failed">
        <XCircleIcon size={27} className={styles.errorIcon} />
      </span>
    );
  }
  return <span />;
};

export default TestStatus;
