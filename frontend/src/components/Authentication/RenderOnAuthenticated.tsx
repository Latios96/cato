import React, { PropsWithChildren } from "react";
import { useUser } from "../../contexts/AuthenticatedUserContext/UserContext";

function RenderOnAuthenticated(props: PropsWithChildren<{}>) {
  const userContext = useUser();
  return <>{userContext !== undefined ? props.children : null}</>;
}

export default RenderOnAuthenticated;
