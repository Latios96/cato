import React from "react";
import { OS } from "../../../../catoapimodels/catoapimodels";
import {
  Apple,
  QuestionCircle,
  Ubuntu,
  Window,
  Windows,
} from "react-bootstrap-icons";
import WrapTitle from "../../../../components/WrapTitle/WrapTitle";

interface Props {
  os: OS;
}

function OsInformation(props: Props) {
  switch (props.os) {
    case OS.LINUX:
      return <Ubuntu />;
    case OS.MAC_OS:
      return <Apple />;
    case OS.WINDOWS:
      return <Windows />;
    default:
      return (
        <WrapTitle title={"OS is unknown"}>
          <QuestionCircle />
        </WrapTitle>
      );
  }
}

export default OsInformation;
