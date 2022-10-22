import React from "react";
import { BasicRunInformation } from "../../../../../catoapimodels/catoapimodels";
import GithubActionsInformation from "./GithubActionsInformation";
import OsInformation from "./OsInformation";

interface Props {
  runInformation: BasicRunInformation;
}

function RunInformation(props: Props) {
  return (
    <>
      <OsInformation os={props.runInformation.os} />
      {props.runInformation.runInformationType === "GITHUB_ACTIONS" ? (
        <GithubActionsInformation runInformation={props.runInformation} />
      ) : null}
    </>
  );
}

export default RunInformation;
