import React from "react";
import {
  Page,
  PageRequest,
  requestFirstPageOfSize,
} from "../../../components/Pagination/Page";
import { RunDto } from "../../../catoapimodels";
import RunListImplementation from "./RunListImplementation";
import { useReFetch } from "../../../hooks/useReFetch";
import { useHistory } from "react-router-dom";
import queryString from "query-string";
import { updateQueryString } from "../../../utils/queryStringUtils";
interface Props {
  projectId: number;
}
interface State {
  page: PageRequest;
}
function parseStateFromQueryString(theQueryString: string): State {
  const queryParams = queryString.parse(theQueryString, {
    parseNumbers: true,
  });
  const state = { page: requestFirstPageOfSize(25), branch: new Set<string>() };

  if (queryParams.page_number && queryParams.page_size) {
    state.page.page_size = Number(queryParams.page_size);
    state.page.page_number = Number(queryParams.page_number);
  }
  return state;
}

function RunList(props: Props) {
  const history = useHistory();
  const state = parseStateFromQueryString(history.location.search);

  const { loading, error, data } = useReFetch<Page<RunDto>>(
    `/api/v1/runs/project/${props.projectId}?page_number=${state.page.page_number}&page_size=${state.page.page_size}`,
    5000,
    [state.page.page_size, state.page.page_number]
  );

  return (
    <RunListImplementation
      projectId={props.projectId}
      runs={data}
      isLoading={loading}
      error={error}
      pageChangedCallback={(page) => {
        history.push({
          search: updateQueryString(history.location.search, {
            page_number: page.page_number,
            page_size: page.page_size,
          }),
        });
      }}
    />
  );
}

export default RunList;
