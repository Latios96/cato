import React from "react";
import TestResult from "../../models/TestResult";
import { Check, Hourglass } from "react-bootstrap-icons";
import RenderingBucketIcon from "../icons/RenderingBucketIcon";
import { XCircleIcon } from "@primer/octicons-react";
import styles from "./StatusStyles.module.scss";
interface Props {
  restResult: TestResult;
}
const TestStatus = (props: Props) => {
  let status = (props: Props) => {
    if (props.restResult.execution_status === "NOT_STARTED") {
      return <Hourglass size={27} />;
    } else if (props.restResult.execution_status === "RUNNING") {
      return <RenderingBucketIcon isActive={false} />;
    } else if (props.restResult.status === "SUCCESS") {
      return <Check color="green" size={27} />;
    } else if (props.restResult.status === "FAILED") {
      return <XCircleIcon size={27} className={styles.errorIcon} />;
    }
  };
  return <React.Fragment>{status(props)}</React.Fragment>;
};

export default TestStatus;
