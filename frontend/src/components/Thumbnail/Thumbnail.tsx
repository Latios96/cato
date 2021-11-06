import React from "react";
import { CardImage } from "react-bootstrap-icons";
import styles from "./Thumbnail.module.scss";
interface Props {
  url?: string;
  width: string;
  height: string;
}
export function Thumbnail(props: Props) {
  if (!props.url) {
    return (
      <div
        className={styles.thumbnailPlaceholder}
        style={{
          width: props.width,
          height: props.height,
          backgroundImage: `url("${props.url}")`,
        }}
      >
        <CardImage size={"25px"} />
      </div>
    );
  }
  return (
    <div
      className={styles.thumbnail}
      style={{
        width: props.width,
        height: props.height,
        backgroundImage: `url("${props.url}")`,
      }}
    />
  );
}
