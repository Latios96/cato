import React from "react";
import styles from "./LoginPage.module.scss";
// @ts-ignore
import video from "./cato_login_keyvisual_animation_1080p.mp4";

function LoginPage() {
  return (
    <div className={styles.loginBackground}>
      <video className={styles.videoBackground} autoPlay muted loop>
        <source src={video} type="video/mp4" />
      </video>
      <div className={styles.loginContainer}>
        <span className={styles.logo}>cato</span>
        <a
          id={"login"}
          className="btn btn-primary"
          href={`/login?from=${window.location.pathname}`}
        >
          Login
        </a>
      </div>
    </div>
  );
}

export default LoginPage;
