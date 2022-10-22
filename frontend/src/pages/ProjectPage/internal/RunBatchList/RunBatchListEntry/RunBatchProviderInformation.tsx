import React from "react";
import { RunBatchProvider } from "../../../../../catoapimodels/catoapimodels";
import { Github, Pc, QuestionCircle } from "react-bootstrap-icons";
import WrapTitle from "../../../../../components/WrapTitle/WrapTitle";

interface Props {
  runBatchProvider: RunBatchProvider;
}

function RunBatchProviderInformation(props: Props) {
  switch (props.runBatchProvider) {
    case "LOCAL_COMPUTER":
      return (
        <WrapTitle title={"Local Computer"}>
          <Pc size={20} />
        </WrapTitle>
      );
    case "GITHUB_ACTIONS":
      return (
        <WrapTitle title={"Github Actions"}>
          <Github size={20} />
        </WrapTitle>
      );
    default:
      return (
        <WrapTitle title={"Unknown provider"}>
          <QuestionCircle />
        </WrapTitle>
      );
  }
}

export default RunBatchProviderInformation;
