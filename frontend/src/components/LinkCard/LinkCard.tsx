import React, { PropsWithChildren } from "react";
import { Link } from "react-router-dom";
import styles from "./LinkCard.module.scss";
import Skeleton from "react-loading-skeleton";

interface Props {
  name?: string;
  linkTo?: string;
  isLoading?: boolean;
}

const LinkCardImpl = (props: PropsWithChildren<{}>) => {
  return (
    <div className={styles.linkCard}>
      <div className={styles.cardContentDiv}>{props.children}</div>
    </div>
  );
};

const LinkCard = (props: Props) => {
  return (
    <Link to={props.linkTo || ""} style={{ textDecoration: "none" }}>
      <LinkCardImpl>
        {props.isLoading ? (
          <Skeleton count={1} width={200} height={25} />
        ) : (
          <>{props.name || ""}</>
        )}
      </LinkCardImpl>
    </Link>
  );
};

export default LinkCard;
