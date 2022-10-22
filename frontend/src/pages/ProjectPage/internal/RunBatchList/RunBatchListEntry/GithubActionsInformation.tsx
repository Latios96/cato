import React from "react";
import { BoxArrowInUpRight } from "react-bootstrap-icons";
import { GithubActionsRunInformation } from "../../../../../catoapimodels/catoapimodels";

interface Props {
  runInformation: GithubActionsRunInformation;
}

function GithubActionsInformation(props: Props) {
  return (
    <>
      <a
        href={props.runInformation.htmlUrl}
        target={"_blank"}
        rel="noopener noreferrer"
        title={"View run on Github Actions"}
      >
        <BoxArrowInUpRight />
      </a>
    </>
  );
}

export default GithubActionsInformation;
