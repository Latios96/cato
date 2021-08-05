import React, { useState } from "react";
import { CachePolicies, useFetch } from "use-http";
import {
  Page,
  requestFirstPageOfSize,
} from "../../../components/Pagination/Page";
import { RunDto } from "../../../catoapimodels";
import RunListImplementation from "./RunListImplementation";
interface Props {
  projectId: number;
}

function RunList(props: Props) {
  const [currentPage, setCurrentPage] = useState(requestFirstPageOfSize(25));
  const { loading, error, data } = useFetch<Page<RunDto>>(
    `/api/v1/runs/project/${props.projectId}?page_number=${currentPage.page_number}&page_size=${currentPage.page_size}`,
    { cachePolicy: CachePolicies.NO_CACHE },
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
      }}
    />
  );
}

export default RunList;
