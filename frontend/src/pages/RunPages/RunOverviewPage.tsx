import React from "react";
import BasicRunPage from "./internal/BasicRunPage";
import { CurrentPage } from "./internal/CurrentPage";
import InfoBox from "../../components/InfoBox/InfoBox";
import InfoBoxElement from "../../components/InfoBox/InfoBoxElement/InfoBoxElement";
import { formatDuration } from "../../utils";
import { CachePolicies, useFetch } from "use-http";
import { RunSummaryDto } from "../../catoapimodels";

interface Props {
  projectId: number;
  runId: number;
}

function RunOverviewPage(props: Props) {
  const { data: runSummaryDto } = useFetch<RunSummaryDto>(
    `/api/v1/runs/${props.runId}/summary`,
    {
      cachePolicy: CachePolicies.NO_CACHE,
    },
    []
  );

  return (
    <BasicRunPage {...props} currentPage={CurrentPage.OVERVIEW}>
      {runSummaryDto ? (
        <InfoBox>
          <InfoBoxElement
            value={"" + runSummaryDto.suite_count}
            title={"suites"}
          />
          <InfoBoxElement
            value={"" + runSummaryDto.test_count}
            title={"tests"}
          />
          <InfoBoxElement
            value={"" + runSummaryDto.failed_test_count}
            title={"failed tests"}
          />
          <InfoBoxElement
            value={
              "" +
              formatDuration(
                runSummaryDto.duration !== "NaN" ? runSummaryDto.duration : 0
              )
            }
            title={"duration"}
          />
        </InfoBox>
      ) : null}
    </BasicRunPage>
  );
}

export default RunOverviewPage;
