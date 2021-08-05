import React from "react";
import styles from "./Footer.module.scss";
interface Props {}

function Footer(props: Props) {
  return (
    <div className={`${styles.footer}`}>
      <div>
        <span>Cato</span>
        <span>Build info</span>
      </div>
    </div>
  );
}

export default Footer;
