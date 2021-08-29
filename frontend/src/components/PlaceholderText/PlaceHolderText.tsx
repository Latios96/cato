import React from "react";
import styles from "./PlaceHolderText.module.scss";
interface Props {
  text: string;
  className?: string;
}
const PlaceHolderText = (props: Props) => {
  return (
    <span className={`${styles.placeholderText} ${props.className}`}>
      {props.text}
    </span>
  );
};

export default PlaceHolderText;
