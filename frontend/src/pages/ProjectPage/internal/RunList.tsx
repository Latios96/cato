import React from "react";
import {
  Page,
  PageRequest,
  requestFirstPageOfSize,
} from "../../../components/Pagination/Page";
import RunListImplementation from "./RunListImplementation";
import { useReFetch } from "../../../hooks/useReFetch";
import { useHistory } from "react-router-dom";
import queryString from "query-string";
import {
  popFromQueryString,
  updateQueryString,
} from "../../../utils/queryStringUtils";
import { fromCommaSeparatedString, toCommaSeparatedString } from "./utils";
import { RunDto } from "../../../catoapimodels/catoapimodels";
interface Props {
  projectId: number;
}
interface State {
  page: PageRequest;
  branches: Set<string>;
}
function parseStateFromQueryString(theQueryString: string): State {
  // todo extract and tests
  const queryParams = queryString.parse(theQueryString, {
    parseNumbers: true,
  });
  const state = {
    page: requestFirstPageOfSize(25),
    branches: new Set<string>(),
  };

  if (queryParams.pageNumber && queryParams.pageSize) {
    state.page.pageSize = Number(queryParams.pageSize);
    state.page.pageNumber = Number(queryParams.pageNumber);
  }
  if (queryParams.branches) {
    state.branches = fromCommaSeparatedString("" + queryParams.branches);
  }
  return state;
}

function RunList(props: Props) {
  const history = useHistory();
  const state = parseStateFromQueryString(history.location.search);

  const {
    isLoading: loadingRuns,
    error: errorRuns,
    data: runs,
  } = useReFetch<Page<RunDto>>(
    `/api/v1/runs/project/${props.projectId}?pageNumber=${
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
    <RunListImplementation
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

export default RunList;
