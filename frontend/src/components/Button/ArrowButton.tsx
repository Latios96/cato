import React from "react";
import {
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  ChevronUp,
} from "react-bootstrap-icons";

import styles from "./ArrowButton.module.scss";

type Direction = "up" | "down" | "left" | "right";

interface Props {
  text?: string;
  direction: Direction;
  onClick?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
}

function directionToIcon(direction: Direction) {
  if (direction === "up") {
    return <ChevronUp />;
  } else if (direction === "down") {
    return <ChevronDown />;
  } else if (direction === "left") {
    return <ChevronLeft />;
  } else if (direction === "right") {
    return <ChevronRight />;
  }
}

function ArrowButton(props: Props) {
  return (
    <button className={styles.arrowButton} onClick={props.onClick}>
      {props.text} {directionToIcon(props.direction)}
    </button>
  );
}

export default ArrowButton;
