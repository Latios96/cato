import React from "react";
import styles from "./Header.module.scss";
import { Link } from "react-router-dom";

interface Props {}

function Header(props: Props) {
  return (
    <div className={styles.header}>
      <Link to={"/"}>
        <div className={styles.logo}>
          <span className={styles.logoCato}>cato</span>
        </div>
      </Link>
    </div>
  );
}

export default Header;
