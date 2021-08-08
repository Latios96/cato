import React from "react";
import BasicRunPage from "./internal/BasicRunPage";
import { CurrentPage } from "./internal/CurrentPage";
import { RunSummary } from "./internal/RunSummary";

interface Props {
  projectId: number;
  runId: number;
}

function RunOverviewPage(props: Props) {
  return (
    <BasicRunPage {...props} currentPage={CurrentPage.OVERVIEW}>
      <RunSummary runId={props.runId} />
    </BasicRunPage>
  );
}

export default RunOverviewPage;
