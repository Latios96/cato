import { useQuery } from "react-query";
import { AuthUser } from "../../catoapimodels/catoapimodels";
import React, { PropsWithChildren, useContext } from "react";

const UserContext = React.createContext<AuthUser | undefined>(undefined);

export function useUser() {
  return useContext<AuthUser | undefined>(UserContext);
}

export function UserProvider(props: PropsWithChildren<{}>) {
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
