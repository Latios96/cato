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
  id?: string;
  text?: string;
  direction: Direction;
  onClick?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
  color?: string;
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
    <button
      id={props.id}
      className={styles.arrowButton}
      onClick={props.onClick}
      style={{ color: props.color || "#0f5b99" }}
    >
      {props.text} {directionToIcon(props.direction)}
    </button>
  );
}

export default ArrowButton;
