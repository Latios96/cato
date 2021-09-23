import React from "react";
import { Spinner as BootStrapSpinner } from "react-bootstrap";
interface Props {
  radius?: string;
}

function Spinner(props: Props) {
  const size = props.radius || "22px";
  return (
    <BootStrapSpinner
      animation="border"
      role="status"
      style={{
        width: size,
        height: size,
        border: "1px solid #ff008c",
        borderRightColor: "transparent",
      }}
    />
  );
}

export default Spinner;
