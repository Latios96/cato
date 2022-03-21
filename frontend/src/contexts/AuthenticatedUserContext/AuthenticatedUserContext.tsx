import { useQuery } from "react-query";
import { AuthUser } from "../../catoapimodels/catoapimodels";
import React, { PropsWithChildren, useContext } from "react";

const UserContext = React.createContext<AuthUser>({
  id: 0,
  email: "",
  username: "",
  fullname: "",
});

export function useUserContext() {
  return useContext<AuthUser>(UserContext);
}

export function AuthenticatedUserProvider(props: PropsWithChildren<{}>) {
  const { data: user } = useQuery<AuthUser, string>("about", () =>
    fetch("/api/v1/users/whoami").then((res) =>
      res.status === 200 ? res.json() : undefined
    )
  );

  if (!user) {
    return <>{props.children}</>;
  }

  return (
    <UserContext.Provider value={user}>{props.children}</UserContext.Provider>
  );
}
