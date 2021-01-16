import React from "react";
import styles from "./FailureMessageBox.module.scss";
import RenderingBucketIcon from "../icons/RenderingBucketIcon";
import { formatTime } from "../../utils";
interface Props {
  startedAt: string | undefined | null;
}
const IsRenderingMessageBox = (props: Props) => {
  return (
    <div className={styles.infoMessageBox}>
      <RenderingBucketIcon isActive={false} />
      <span className={styles.messageText}>{`started: ${
        props.startedAt ? formatTime(props.startedAt) : "unkown"
      }`}</span>
    </div>
  );
};

export default IsRenderingMessageBox;
