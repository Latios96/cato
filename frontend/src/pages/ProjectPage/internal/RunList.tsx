import React, { useState } from "react";
import {
  Page,
  requestFirstPageOfSize,
} from "../../../components/Pagination/Page";
import { RunDto } from "../../../catoapimodels";
import RunListImplementation from "./RunListImplementation";
import { useReFetch } from "../../../hooks/useReFetch";
import { useHistory } from "react-router-dom";
import {
  fromQueryString,
  toQueryString,
} from "../../../components/Pagination/pageQueryStringUtils";
interface Props {
  projectId: number;
}

function RunList(props: Props) {
  const history = useHistory();
  const page = fromQueryString(
    history.location.search.substring(1),
    requestFirstPageOfSize(25)
  );

  const [currentPage, setCurrentPage] = useState(page);
  const { loading, error, data } = useReFetch<Page<RunDto>>(
    `/api/v1/runs/project/${props.projectId}?page_number=${currentPage.page_number}&page_size=${currentPage.page_size}`,
    5000,
    [currentPage]
  );

  return (
    <RunListImplementation
      projectId={props.projectId}
      runs={data}
      isLoading={loading}
      error={error}
      pageChangedCallback={(page) => {
        setCurrentPage(page);
        history.push({ search: "?" + toQueryString(page) });
      }}
    />
  );
}

export default RunList;
