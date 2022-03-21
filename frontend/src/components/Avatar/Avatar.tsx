import React from "react";
import { AuthUser } from "../../catoapimodels/catoapimodels";
import styles from "./Avatar.module.scss";

interface Props {
  user: AuthUser;
  radius?: number;
}

function Avatar(props: Props) {
  const radius = props.radius || 32;
  let splittedBySpace = props.user.fullname.split(" ");
  const firstName = splittedBySpace[0][0];
  const lastName = splittedBySpace[splittedBySpace.length - 1][0];
  return (
    <div
      style={{
        width: radius,
        height: radius,
        borderRadius: radius,
        fontSize: radius / 2,
      }}
      className={styles.avatar}
    >
      {firstName.toUpperCase()}
      {lastName.toUpperCase()}
    </div>
  );
}

export default Avatar;
