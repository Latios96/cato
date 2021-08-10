import React, { useState } from "react";
import {
  Page,
  requestFirstPageOfSize,
} from "../../../components/Pagination/Page";
import { RunDto } from "../../../catoapimodels";
import RunListImplementation from "./RunListImplementation";
import { useReFetch } from "../../../hooks/useReFetch";
interface Props {
  projectId: number;
}

function RunList(props: Props) {
  const [currentPage, setCurrentPage] = useState(requestFirstPageOfSize(25));
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
      }}
    />
  );
}

export default RunList;
