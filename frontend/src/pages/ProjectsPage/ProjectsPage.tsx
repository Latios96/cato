import React from "react";
import { ProjectsView } from "./internal/ProjectsView/ProjectsView";
import BasicPage from "../BasicPage";

interface Props {}

function ProjectsPage(props: Props) {
  return (
    <BasicPage title={"Projects"}>
      <ProjectsView />
    </BasicPage>
  );
}

export default ProjectsPage;
