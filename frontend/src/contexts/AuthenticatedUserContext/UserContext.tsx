import { AuthUser } from "../../catoapimodels/catoapimodels";
import React, { PropsWithChildren, useContext } from "react";
import { useFetch } from "../../hooks/useFetch";

const UserContext = React.createContext<AuthUser | undefined>(undefined);

export function useUser() {
  return useContext<AuthUser | undefined>(UserContext);
}

export function UserProvider(props: PropsWithChildren<{}>) {
  const { data: user } = useFetch<AuthUser>("/api/v1/users/whoami");

  if (!user) {
    return <>{props.children}</>;
  }

  return (
    <UserContext.Provider value={user}>{props.children}</UserContext.Provider>
  );
}
