import React from "react";
import ProjectRunsView from "../components/ProjectRunView/ProjectRunsView";
import BasicPage from "./BasicPage";

interface Props {
  projectId: number;
  currentRunId: number | null;
  currentTab: string | null;
  suiteOrTestId: number | null;
}

function ProjectPage(props: Props) {
  return (
    <BasicPage>
      <ProjectRunsView
        projectId={props.projectId}
        currentRunId={props.currentRunId}
        currentTab={props.currentTab}
        suiteOrTestId={props.suiteOrTestId}
      />
    </BasicPage>
  );
}

export default ProjectPage;
