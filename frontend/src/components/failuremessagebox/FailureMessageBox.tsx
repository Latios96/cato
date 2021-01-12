import React from "react";
import styles from "./FailureMessageBox.module.scss";
import { ExclamationCircleFill } from "react-bootstrap-icons";
interface Props {
  message: string | null | undefined;
}
const FailureMessageBox = (props: Props) => {
  return (
    <div className={styles.messageBox}>
      <ExclamationCircleFill size={22} />
      <span className={styles.messageText}>{props.message}</span>
    </div>
  );
};

export default FailureMessageBox;
