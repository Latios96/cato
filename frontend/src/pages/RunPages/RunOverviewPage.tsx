import React from "react";
import BasicRunPage from "./internal/BasicRunPage";
import { CurrentPage } from "./internal/CurrentPage";
import { CachePolicies, useFetch } from "use-http";
import { RunSummaryDto } from "../../catoapimodels";
import { RunSummary } from "./internal/RunSummary";
import {
  LoadingStateHandler,
  LoadingState,
  ErrorState,
  DataLoaded,
} from "./internal/LoadingStateHandler";

interface Props {
  projectId: number;
  runId: number;
}

function RunOverviewPage(props: Props) {
  return (
    <BasicRunPage {...props} currentPage={CurrentPage.OVERVIEW}>
      <RunSummary runId={props.runId} />
      <LoadingStateHandler>
        <LoadingState />
        <ErrorState />
        <DataLoaded />
      </LoadingStateHandler>
    </BasicRunPage>
  );
}

export default RunOverviewPage;
