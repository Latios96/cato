import { AuthUser } from "../../catoapimodels/catoapimodels";
import React, { PropsWithChildren, useContext } from "react";
import { useFetch } from "../../hooks/useFetch";
interface AuthUserContext {
  user?: AuthUser;
  isLoading: boolean;
}
const UserContext = React.createContext<AuthUserContext>({ isLoading: true });

export function useUser() {
  return useContext<AuthUserContext>(UserContext);
}

export function UserProvider(props: PropsWithChildren<{}>) {
  const { data: user, isLoading } = useFetch<AuthUser>("/api/v1/users/whoami");
  return (
    <UserContext.Provider value={{ user, isLoading }}>
      {props.children}
    </UserContext.Provider>
  );
}
