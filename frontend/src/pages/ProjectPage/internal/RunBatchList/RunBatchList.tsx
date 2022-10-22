import React from "react";
import { Page } from "../../../../components/Pagination/Page";
import { useReFetch } from "../../../../hooks/useReFetch";
import { useHistory } from "react-router-dom";
import {
  popFromQueryString,
  updateQueryString,
} from "../../../../utils/queryStringUtils";
import { toCommaSeparatedString } from "../utils";
import { RunBatchAggregate } from "../../../../catoapimodels/catoapimodels";
import RunBatchListImplementation from "./RunBatchListImplementation";
import { parseStateFromQueryString } from "./queryStringState";

interface Props {
  projectId: number;
}

function RunBatchList(props: Props) {
  const history = useHistory();
  const state = parseStateFromQueryString(history.location.search);

  const {
    isLoading: loadingRuns,
    error: errorRuns,
    data: runs,
  } = useReFetch<Page<RunBatchAggregate>>(
    `/api/v1/run_batches/project/${props.projectId}?pageNumber=${
      state.page.pageNumber
    }&pageSize=${state.page.pageSize}&branches=${toCommaSeparatedString(
      state.branches
    )}`,
    5000,
    [
      state.page.pageSize,
      state.page.pageNumber,
      toCommaSeparatedString(state.branches),
    ]
  );

  const { data: branches } = useReFetch<string[]>(
    `/api/v1/runs/project/${props.projectId}/branches`,
    5000,
    []
  );

  return (
    <RunBatchListImplementation
      projectId={props.projectId}
      runs={runs}
      isLoading={loadingRuns}
      error={errorRuns}
      pageChanged={(page) => {
        history.push({
          // todo can we make this better?
          search: updateQueryString(history.location.search, {
            pageNumber: page.pageNumber,
            pageSize: page.pageSize,
          }),
        });
      }}
      filteredBranchesChanged={(branches) => {
        let search = "";
        if (!branches.size) {
          search = popFromQueryString(history.location.search, ["branches"]);
        } else {
          search = updateQueryString(history.location.search, {
            branches: Array.from(branches).sort().join(","),
          });
        }
        history.push({ search });
      }}
      branches={branches || []}
      selectedBranches={state.branches}
    />
  );
}

export default RunBatchList;
