import React from "react";
import styles from "./Header.module.css";

interface Props {}

function Header(props: Props) {
  return (
    <div className={styles.header}>
      <div className={styles.logo}>
        <span className={styles.logoCato}>cato</span>
      </div>
    </div>
  );
}

export default Header;
