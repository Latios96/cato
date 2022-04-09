import React, { PropsWithChildren } from "react";
import styles from "./InfoBox.module.scss";
import { joinClassnames } from "../../utils/classnameUtils";

interface Props {
  className?: string;
}

const InfoBox = (props: PropsWithChildren<Props>) => {
  return (
    <div className={joinClassnames([styles.infoBox, props.className])}>
      {props.children}
    </div>
  );
};

export default InfoBox;
