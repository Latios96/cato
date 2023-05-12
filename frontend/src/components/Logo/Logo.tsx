import React from "react";
import { ReactComponent as LogoWhite } from "./LogoWhite.svg";

interface Props {
  height: number;
}

function Logo(props: Props) {
  return <LogoWhite height={props.height} />;
}

export default Logo;
