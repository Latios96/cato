import React from "react";
import styles from "./LoginPage.module.scss";

function LoginPage() {
  return (
    <div className={styles.loginBackground}>
      <div className={styles.loginContainer}>
        <span className={styles.logo}>cato</span>
        <a className="btn btn-primary" href={"/login"}>
          Login
        </a>
      </div>
    </div>
  );
}

export default LoginPage;
