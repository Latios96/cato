import React, { PropsWithChildren } from "react";
import styles from "./Button.module.scss";

interface Props {
  primary?: boolean;
  onClick?: () => void;
  disabled?: boolean;
}

const Button = (props: PropsWithChildren<Props>) => {
  return (
    <button
      className={styles.button}
      onClick={props.onClick}
      disabled={props.disabled}
      data-primary={props.primary}
    >
      {props.children}
    </button>
  );
};

export default Button;
