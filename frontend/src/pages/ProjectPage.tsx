import React from "react";
import Header from "../components/header/Header";
import ProjectsView from "../components/projectsview/ProjectsView";
import ProjectRunsView from "../components/projectrunview/ProjectRunsView";

interface Props {
  projectId: number;
}

function ProjectsPage(props: Props) {
  return (
    <div>
      <Header />
      <ProjectRunsView projectId={props.projectId} />{" "}
    </div>
  );
}

export default ProjectsPage;
