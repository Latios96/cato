import React from "react";
import styles from "./Header.module.scss";
import { Link } from "react-router-dom";
import { LoginButton } from "../LoginButton/LoginButton";
import { AboutUserMenu } from "./AboutUserMenu";
import RenderOnAnonymous from "../Authentication/RenderOnAnonymous";
import RenderOnAuthenticated from "../Authentication/RenderOnAuthenticated";

interface Props {}

function Header(props: Props) {
  return (
    <div className={styles.header}>
      <Link to={"/"}>
        <div className={styles.logo}>
          <span className={styles.logoCato}>cato</span>
        </div>
      </Link>
      <span
        className={"d-flex flex-column justify-content-center ml-auto mr-3"}
      >
        <RenderOnAnonymous render={() => <LoginButton />} />
        <RenderOnAuthenticated render={() => <AboutUserMenu />} />
      </span>
      )
    </div>
  );
}

export default Header;
