import React from "react";
import styles from "./Header.module.scss";
import { Link } from "react-router-dom";
import { useUserContext } from "../../contexts/AuthenticatedUserContext/AuthenticatedUserContext";
import { LoginButton } from "../LoginButton/LoginButton";
import { AboutUserMenu } from "./AboutUserMenu";

interface Props {}

function Header(props: Props) {
  const userContext = useUserContext();
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
        {userContext.id === 0 ? (
          <LoginButton />
        ) : (
          <AboutUserMenu user={userContext} />
        )}
      </span>
      )
    </div>
  );
}

export default Header;
