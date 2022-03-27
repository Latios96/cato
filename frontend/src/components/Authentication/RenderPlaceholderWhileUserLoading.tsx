import React from "react";
import { useUser } from "../../contexts/AuthenticatedUserContext/UserContext";
interface Props {
  renderWhenLoaded: () => JSX.Element;
}
function RenderPlaceholderWhileUserLoading(props: Props) {
  const userContext = useUser();
  if (userContext.isLoading) {
    return <></>;
  }
  return <>{props.renderWhenLoaded()}</>;
}

export default RenderPlaceholderWhileUserLoading;
