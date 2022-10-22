import React from "react";
import { OS } from "../../../../catoapimodels/catoapimodels";
import { Apple, QuestionCircle, Ubuntu, Windows } from "react-bootstrap-icons";
import WrapTitle from "../../../../components/WrapTitle/WrapTitle";

interface Props {
  os: OS;
}

function OsInformation(props: Props) {
  switch (props.os) {
    case OS.LINUX:
      return (
        <WrapTitle title={"Linux"}>
          <Ubuntu />
        </WrapTitle>
      );
    case OS.MAC_OS:
      return (
        <WrapTitle title={"Mac OS"}>
          <Apple />
        </WrapTitle>
      );
    case OS.WINDOWS:
      return (
        <WrapTitle title={"Windows"}>
          <Windows />
        </WrapTitle>
      );
    default:
      return (
        <WrapTitle title={"OS is unknown"}>
          <QuestionCircle />
        </WrapTitle>
      );
  }
}

export default OsInformation;
