import Avatar from "../Avatar/Avatar";
import ArrowButton from "../Button/ArrowButton";
import React from "react";
import axios from "axios";
import { useAuthenticatedUser } from "../../contexts/AuthenticatedUserContext/AuthenticatedUserContext";
import PopoverMenu from "../PopoverMenu/PopoverMenu";

export function AboutUserMenu() {
  const authenticatedUser = useAuthenticatedUser();
  return (
    <PopoverMenu
      id={"about-user-menu"}
      menuItems={[
        {
          id: "username",
          element: (
            <>
              <span className={"font-weight-bolder"}>
                {authenticatedUser.fullname}
              </span>
              <span>@{authenticatedUser.username}</span>
            </>
          ),
        },
        {
          id: "logout",
          element: <>Logout</>,
          onClick: () => {
            axios
              .post("/logout")
              .then(() => {
                window.location.href = "/";
              })
              .catch(() => {});
          },
        },
      ]}
      menuTriggerElement={
        <div className={"d-flex"}>
          <Avatar user={authenticatedUser} />
          <ArrowButton
            id={"btn-about-user-menu"}
            direction={"down"}
            color={"white"}
          />
        </div>
      }
    />
  );
}
