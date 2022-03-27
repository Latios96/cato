import React from "react";
import { useUser } from "../../contexts/AuthenticatedUserContext/UserContext";
interface Props {
  render: () => JSX.Element;
}
function RenderOnAuthenticated(props: Props) {
  const { user } = useUser();
  return <>{user !== undefined ? props.render() : null}</>;
}

export default RenderOnAuthenticated;
