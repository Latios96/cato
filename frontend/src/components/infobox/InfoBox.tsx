import React from "react";
import styles from "./InfoBox.module.scss";

interface Props {
  className?: string;
}

const InfoBox: React.FunctionComponent<Props> = (props) => {
  return (
    <div className={styles.infoBox + " " + props.className}>
      {props.children}
    </div>
  );
};

export default InfoBox;
