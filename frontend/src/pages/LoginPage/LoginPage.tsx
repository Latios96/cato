import React from "react";
import { Button } from "react-bootstrap";
import styles from "./LoginPage.module.scss";

function LoginPage() {
  return (
    <div className={styles.loginBackground}>
      <div className={styles.loginContainer}>
        <span className={styles.logo}>cato</span>
        <Button>Login</Button>
      </div>
    </div>
  );
}

export default LoginPage;
