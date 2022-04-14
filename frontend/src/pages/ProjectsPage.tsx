import React from "react";
import { ProjectsView } from "../components/ProjectsView/ProjectsView";
import BasicPage from "./BasicPage";

interface Props {}

function ProjectsPage(props: Props) {
  return (
    <BasicPage title={"Projects"}>
      <ProjectsView />
    </BasicPage>
  );
}

export default ProjectsPage;
