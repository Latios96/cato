import React from "react";
import Header from "../components/header/Header";
import ProjectRunsView from "../components/projectrunview/ProjectRunsView";

interface Props {
  projectId: number;
  currentRunId: number | null;
}

function ProjectPage(props: Props) {
  return (
    <div>
      <Header />
      <ProjectRunsView
        projectId={props.projectId}
        currentRunId={props.currentRunId}
      />
    </div>
  );
}

export default ProjectPage;
