import React from "react";
import { Link } from "react-router-dom";
import styles from "./LinkCard.module.css";

interface Props {
  name: string;
  linkTo: string;
}

const LinkCard = (props: Props) => {
  return (
    <Link to={props.linkTo}>
      <div className={styles.linkCard}>
        <div className={styles.cardContentDiv}>{props.name}</div>
      </div>
    </Link>
  );
};

export default LinkCard;
