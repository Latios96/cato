import React from "react";
import styles from "./RenderingBucketIcon.module.css";
import bucket_anim from "./bucket_anim.gif";

function RenderingBucketIcon() {
  return <img className={styles.bucketAnimImage} src={bucket_anim} />;
}

export default RenderingBucketIcon;
