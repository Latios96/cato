import React from "react";
import styles from "./RenderingBucketIcon.module.css";
import bucket_anim_white_on_black from "./bucket_anim_white_on_black.gif";
import bucket_anim_black_on_white from "./bucket_anim_black_on_white.gif";

interface Props {
  isActive: boolean;
}

function RenderingBucketIcon(props: Props) {
  {
    return props.isActive ? (
      <img
        className={styles.bucketAnimImage}
        src={bucket_anim_white_on_black}
        alt={"an animated rendering icon"}
      />
    ) : (
      <img
        className={styles.bucketAnimImage}
        src={bucket_anim_black_on_white}
        alt={"an animated rendering icon"}
      />
    );
  }
}

export default RenderingBucketIcon;
