import React from "react";
import styles from "./FailureMessageBox.module.scss";
import { Hourglass } from "react-bootstrap-icons";
interface Props {
  message: string | null | undefined;
}
const InfoMessageBox = (props: Props) => {
  return (
    <div className={styles.infoMessageBox}>
      <Hourglass data-testid={"running-hourglas"} size={27} />
      <span className={styles.messageText}>{props.message}</span>
    </div>
  );
};

export default InfoMessageBox;
