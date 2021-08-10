import React from "react";
import { CircleFill } from "react-bootstrap-icons";
import styles from "./AlphaButton.module.scss";

interface Props {
  isToggled: boolean;
  onClick: () => void;
  clickable: boolean;
}

const AlphaButton = (props: Props) => {
  function getStyle() {
    if (!props.clickable) {
      return `${styles.buttonBg} ${styles.buttonBgDisabled}`;
    }
    return `${styles.buttonBg} ${
      props.isToggled ? styles.buttonBgEnabled : ""
    } ${props.clickable ? styles.buttonBgClickable : ""}`;
  }

  return (
    <div
      className={getStyle()}
      onClick={() => {
        if (props.clickable) {
          props.onClick();
        }
      }}
    >
      <CircleFill
        className={`${styles.icon} ${
          props.isToggled ? styles.iconEnabled : ""
        }`}
      />
    </div>
  );
};

export default AlphaButton;
