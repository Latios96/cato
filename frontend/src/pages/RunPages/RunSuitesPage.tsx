import React from "react";
import { CachePolicies, useFetch } from "use-http";
import { SuiteResultDto } from "../../catoapimodels";
import BasicRunPage from "./internal/BasicRunPage";
import { CurrentPage } from "./internal/CurrentPage";
interface Props {
  projectId: number;
  runId: number;
}

function RunSuitePage(props: Props) {
  const { data } = useFetch<SuiteResultDto[]>(
    `/api/v1/suite_results/run/${props.runId}`,
    {
      cachePolicy: CachePolicies.NO_CACHE,
    },
    []
  );
  return (
    <BasicRunPage {...props} currentPage={CurrentPage.SUITES}>
      <div>
        {data
          ? data.map((suite) => {
              return <p>{suite.suite_name}</p>;
            })
          : ""}
      </div>
    </BasicRunPage>
  );
}

export default RunSuitePage;
