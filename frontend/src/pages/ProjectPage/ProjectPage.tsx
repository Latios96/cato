import React from "react";
import BasicPage from "../BasicPage";
import ProjectInformation from "./internal/ProjectInformation";
import RunBatchList from "./internal/RunBatchList/RunBatchList";

interface Props {
  projectId: number;
}

function ProjectPage(props: Props) {
  return (
    <BasicPage>
      <ProjectInformation projectId={props.projectId} />
      <div
        className={"ml-auto mr-auto "}
        style={{ width: "850px", marginTop: "35px" }}
      ></div>
      <RunBatchList projectId={props.projectId} />
    </BasicPage>
  );
}

export default ProjectPage;
