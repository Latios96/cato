import React from "react";
import styles from "./InfoBox.module.scss";
import { joinClassnames } from "../../utils/classnameUtils";

interface Props {
  className?: string;
}

const InfoBox: React.FunctionComponent<Props> = (props) => {
  return (
    <div className={joinClassnames([styles.infoBox, props.className])}>
      {props.children}
    </div>
  );
};

export default InfoBox;
