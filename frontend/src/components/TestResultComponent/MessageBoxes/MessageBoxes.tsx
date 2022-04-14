import React from "react";
import styles from "./MessageBoxes.module.scss";
import { ExclamationCircleFill, Hourglass } from "react-bootstrap-icons";
import RenderingBucketIcon from "../../Icons/RenderingBucketIcon";
import FormattedTime from "../../FormattedTime/FormattedTime";

interface BasicProps {
  message?: string | null;
  messageElement?: JSX.Element;
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
      <span className={styles.messageText}>
        {props.message || props.messageElement}
      </span>
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
      messageElement={
        <>
          {"started: "}
          {props.startedAt ? (
            <FormattedTime datestr={props.startedAt} />
          ) : (
            "unknown"
          )}
        </>
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
