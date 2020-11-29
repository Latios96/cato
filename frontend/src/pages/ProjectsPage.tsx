import React from "react";
import Header from "../components/header/Header";
import ProjectsView from "../components/projectsview/ProjectsView";

interface Props {}

function ProjectsPage(props: Props) {
  return (
    <div>
      <Header />
      <ProjectsView />
    </div>
  );
}

export default ProjectsPage;
