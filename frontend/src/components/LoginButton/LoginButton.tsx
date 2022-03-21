import Button from "../Button/Button";
import React from "react";

export function LoginButton() {
  return (
    <a
      href={
        `${window.location.origin}/login` /*TODO adjust this once HashRouter is removed*/
      }
    >
      <Button primary>Login</Button>
    </a>
  );
}
