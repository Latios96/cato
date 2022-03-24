import React, { PropsWithChildren } from "react";
import { useUser } from "../../contexts/AuthenticatedUserContext/UserContext";

function RenderOnAnonymous(props: PropsWithChildren<{}>) {
  const userContext = useUser();
  return <>{userContext === undefined ? props.children : null}</>;
}

export default RenderOnAnonymous;
