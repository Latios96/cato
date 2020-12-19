import React from "react";
import Header from "../components/header/Header";
import ProjectRunsView from "../components/projectrunview/ProjectRunsView";

interface Props {
  projectId: number;
  currentRunId: number | null;
  currentTab: string | null;
  suiteOrTestId: number | null;
}

function ProjectPage(props: Props) {
  return (
    <div>
      <Header />
      <ProjectRunsView
        projectId={props.projectId}
        currentRunId={props.currentRunId}
        currentTab={props.currentTab}
        suiteOrTestId={props.suiteOrTestId}
      />
    </div>
  );
}

export default ProjectPage;
