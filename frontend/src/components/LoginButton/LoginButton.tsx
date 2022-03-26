import Button from "../Button/Button";
import React from "react";

export function LoginButton() {
  return (
    <a href={"/login"}>
      <Button primary>Login</Button>
    </a>
  );
}
