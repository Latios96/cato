import React from "react";
import styles from "./MessageBoxes.module.scss";
import { ExclamationCircleFill, Hourglass } from "react-bootstrap-icons";
import { formatTime } from "../../../utils/dateUtils";
import RenderingBucketIcon from "../../Icons/RenderingBucketIcon";

interface BasicProps {
  message: string | null | undefined;
  icon: JSX.Element;
  className?: string;
}

interface Props {
  message: string | null | undefined;
}

const BasicMessageBox = (props: BasicProps) => {
  return (
    <div className={props.className ? props.className : styles.messageBoxBody}>
      {props.icon}
      <span className={styles.messageText}>{props.message}</span>
    </div>
  );
};
export const NotStartedMessageBox = () => {
  return (
    <BasicMessageBox
      message={"waiting to start..."}
      icon={<Hourglass data-testid={"running-hourglas"} size={27} />}
    />
  );
};
interface IsRenderingProps {
  startedAt: string | undefined | null;
}
export const IsRenderingMessageBox = (props: IsRenderingProps) => {
  return (
    <BasicMessageBox
      message={
        "started: " +
        (props.startedAt ? formatTime(props.startedAt) : "unknown")
      }
      icon={<RenderingBucketIcon isActive={false} />}
    />
  );
};
export const FailureMessageBox = (props: Props) => {
  return (
    <BasicMessageBox
      message={props.message}
      className={styles.failureMessageBox}
      icon={<ExclamationCircleFill size={22} />}
    />
  );
};
