import React from "react";
import { useFetch } from "use-http";
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
  const pageRequest = requestFirstPageOfSize(25);
  const { loading, error, data } = useFetch<Page<RunDto>>(
    `/api/v1/runs/project/${props.projectId}?page_number=${pageRequest.page_number}&page_size=${pageRequest.page_size}`,
    []
  );
  return (
    <RunListImplementation
      projectId={props.projectId}
      runs={data}
      isLoading={loading}
      error={error}
    />
  );
}

export default RunList;
