import React from "react";
import styles from "./LoginPage.module.scss";
// @ts-ignore
import video from "./cato_login_keyvisual_animation_1080p.mp4";
import { Helmet } from "react-helmet";
import Logo from "../../components/Logo/Logo";

function LoginPage() {
  return (
    <>
      <Helmet>
        <title>Login</title>
      </Helmet>
      <div className={styles.loginBackground}>
        <video className={styles.videoBackground} autoPlay muted loop>
          <source src={video} type="video/mp4" />
        </video>
        <div className={styles.loginContainer}>
          <Logo height={90} />
          <a
            id={"login"}
            className="btn btn-primary"
            href={`/login?from=${window.location.pathname}`}
          >
            Login
          </a>
        </div>
      </div>
    </>
  );
}

export default LoginPage;
