import React from "react";
import styles from "./Error.module.scss";
interface Props {
  heading: string;
  message: string;
}

function Error(props: Props) {
  return (
    <div className={styles.error}>
      <span>{props.heading}</span>
      <span>{props.message}</span>
    </div>
  );
}

export default Error;
