import React from "react";
import styles from "./InfoBoxElement.module.scss";
interface Props {
  value: string;
  title: string;
  id?: string;
}
const InfoBoxElement = (props: Props) => {
  return (
    <div className={styles.infoBoxElement}>
      <span
        id={props.id ? `${props.id}-value` : ""}
        className={styles.infoBoxValue}
      >
        {props.value}
      </span>
      <span id={props.id ? `${props.id}-value` : ""}>{props.title}</span>
    </div>
  );
};

export default InfoBoxElement;
