import { AuthUser } from "../../catoapimodels/catoapimodels";
import React, { PropsWithChildren, useContext } from "react";
import { useUser } from "./UserContext";

const AuthenticatedUserContext = React.createContext<AuthUser>({
  id: 0,
  email: "",
  username: "",
  fullname: "",
});

export function AuthenticatedUserProvider(props: PropsWithChildren<{}>) {
  const user = useUser();

  if (!user) {
    return <>{props.children}</>;
  }
  return (
    <AuthenticatedUserContext.Provider value={user}>
      {props.children}
    </AuthenticatedUserContext.Provider>
  );
}

export function useAuthenticatedUser() {
  return useContext<AuthUser>(AuthenticatedUserContext);
}
