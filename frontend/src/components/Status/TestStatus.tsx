import React from "react";
import { Check, Hourglass } from "react-bootstrap-icons";
import RenderingBucketIcon from "../Icons/RenderingBucketIcon";
import { XCircleIcon } from "@primer/octicons-react";
import styles from "./StatusStyles.module.scss";
import { TestResultDto } from "../../catoapimodels/catoapimodels";

type TestStatusData = Pick<TestResultDto, "unifiedTestStatus">;

interface Props {
  testResult: TestStatusData;
}
const TestStatus = (props: Props) => {
  if (props.testResult.unifiedTestStatus === "NOT_STARTED") {
    return (
      <span
        className="d-inline-block"
        data-toggle="tooltip"
        title="not started"
      >
        <Hourglass size={27} />
      </span>
    );
  } else if (props.testResult.unifiedTestStatus === "RUNNING") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="running">
        <RenderingBucketIcon isActive={false} />
      </span>
    );
  } else if (props.testResult.unifiedTestStatus === "SUCCESS") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="success">
        <Check color="green" size={27} />
      </span>
    );
  } else if (props.testResult.unifiedTestStatus === "FAILED") {
    return (
      <span className="d-inline-block" data-toggle="tooltip" title="failed">
        <XCircleIcon size={27} className={styles.errorIcon} />
      </span>
    );
  }
  return <span />;
};

export default TestStatus;
