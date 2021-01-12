import React from "react";
import ProjectsView from "../components/projectsview/ProjectsView";
import BasicPage from "./BasicPage";

interface Props {}

function ProjectsPage(props: Props) {
  return (
    <BasicPage>
      <ProjectsView />
    </BasicPage>
  );
}

export default ProjectsPage;
