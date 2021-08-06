import React from "react";
import { CachePolicies, useFetch } from "use-http";
import { TestResultDto } from "../../catoapimodels";
import BasicRunPage from "./internal/BasicRunPage";
import { CurrentPage } from "./internal/CurrentPage";
interface Props {
  projectId: number;
  runId: number;
}

function RunTestsPage(props: Props) {
  const { data } = useFetch<TestResultDto[]>(
    `/api/v1/test_results/run/${props.runId}`,
    {
      cachePolicy: CachePolicies.NO_CACHE,
    },
    []
  );
  return (
    <BasicRunPage {...props} currentPage={CurrentPage.TESTS}>
      <div>
        {data
          ? data.map((test) => {
              return <p>{test.test_identifier}</p>;
            })
          : ""}
      </div>
    </BasicRunPage>
  );
}

export default RunTestsPage;
