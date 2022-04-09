import React from "react";
import { Link } from "react-router-dom";
import styles from "./LinkCard.module.scss";

interface Props {
  name: string;
  linkTo: string;
}

const LinkCard = (props: Props) => {
  return (
    <Link to={props.linkTo} style={{ textDecoration: "none" }}>
      <div className={styles.linkCard}>
        <div className={styles.cardContentDiv} title={props.name}>
          {props.name}
        </div>
      </div>
    </Link>
  );
};

export default LinkCard;
