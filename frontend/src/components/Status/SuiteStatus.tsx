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
  let status = (props: Props) => {
    if (props.suiteResult.status === "NOT_STARTED") {
      return <Hourglass size={27} />;
    } else if (props.suiteResult.status === "RUNNING") {
      return <RenderingBucketIcon isActive={false} />;
    } else if (props.suiteResult.status === "SUCCESS") {
      return <Check color="green" size={27} />;
    } else if (props.suiteResult.status === "FAILED") {
      return <XCircleIcon size={27} className={styles.errorIcon} />;
    }
  };
  return <React.Fragment>{status(props)}</React.Fragment>;
};

export default SuiteStatus;
