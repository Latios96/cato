import React from "react";
import styles from "./ImageDiff.module.scss";
interface Props {
  leftImage: string;
  rightImage: string;
}
const ImageDiff = (props: Props) => {
  return (
    <div className={styles.diffContainer}>
      <img alt="left" className={styles.diffImage} src={props.leftImage} />
      <img
        alt="left"
        className={`${styles.diffImage} ${styles.diffImageDifference}`}
        src={props.rightImage}
      />
    </div>
  );
};

export default ImageDiff;
