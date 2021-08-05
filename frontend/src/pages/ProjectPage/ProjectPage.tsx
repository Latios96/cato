import React from "react";
import BasicPage from "../BasicPage";
import RunList from "./internal/RunList";
import ProjectInformation from "./internal/ProjectInformation";

interface Props {
  projectId: number;
}

function ProjectPage(props: Props) {
  return (
    <BasicPage>
      <ProjectInformation projectId={props.projectId} />
      <RunList projectId={props.projectId} />
    </BasicPage>
  );
}

export default ProjectPage;
