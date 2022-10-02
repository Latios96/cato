import React from "react";
import { BasicRunInformation } from "../../../../catoapimodels/catoapimodels";
import { Pc } from "react-bootstrap-icons";
import GithubActionsInformation from "./GithubActionsInformation";

interface Props {
  runInformation: BasicRunInformation;
}

function RunInformation(props: Props) {
  switch (props.runInformation.runInformationType) {
    case "LOCAL_COMPUTER":
      return <Pc size={20} />;
    case "GITHUB_ACTIONS":
      return <GithubActionsInformation runInformation={props.runInformation} />;
    default:
      return <></>;
  }
}

export default RunInformation;
