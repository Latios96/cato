import { AuthUser } from "../../catoapimodels/catoapimodels";
import { OverlayTrigger } from "react-bootstrap";
import styles from "./AboutUserMenu.module.scss";
import Avatar from "../Avatar/Avatar";
import ArrowButton from "../Button/ArrowButton";
import React from "react";
import axios from "axios";

export function AboutUserMenu(props: { user: AuthUser }) {
  return (
    <OverlayTrigger
      placement="bottom"
      trigger={"click"}
      rootClose={true}
      overlay={
        <div className={styles.inputContainer}>
          <div className={styles.menuContent}>
            <span className={"font-weight-bolder"}>{props.user.fullname}</span>
            <span>@{props.user.username}</span>
          </div>
          <div
            className={styles.menuContent + " " + styles.menuContentClickable}
            onClick={() => {
              axios
                .post("/logout")
                .then(() => {
                  window.location.reload();
                })
                .catch(() => {});
            }}
          >
            <div className={styles.menuElement}>Logout</div>
          </div>
        </div>
      }
    >
      <div className={"d-flex"}>
        <Avatar user={props.user} />
        <ArrowButton direction={"down"} />
      </div>
    </OverlayTrigger>
  );
}
