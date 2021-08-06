import { RunSummaryDto } from "../../../catoapimodels";
import InfoBox from "../../../components/InfoBox/InfoBox";
import InfoBoxElement from "../../../components/InfoBox/InfoBoxElement/InfoBoxElement";
import { formatDuration } from "../../../utils";
import React from "react";

import styles from "./RunSummary.module.scss";
import { CachePolicies, useFetch } from "use-http";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
interface Props {
  runId: number;
}
export function RunSummary(props: Props) {
  const { data: runSummaryDto, loading } = useFetch<RunSummaryDto>(
    `/api/v1/runs/${props.runId}/summary`,
    {
      cachePolicy: CachePolicies.NO_CACHE,
    },
    []
  );

  if (loading) {
    return (
      <div className={styles.runSummary}>
        <SkeletonTheme color="#f7f7f7" highlightColor="white">
          <p>
            <Skeleton count={1} width={720} height={100} />
          </p>
        </SkeletonTheme>
      </div>
    );
  }
  if (!runSummaryDto) {
    return null;
  }

  return (
    <div className={styles.runSummary}>
      <InfoBox>
        <InfoBoxElement
          value={"" + runSummaryDto.suite_count}
          title={"suites"}
        />
        <InfoBoxElement value={"" + runSummaryDto.test_count} title={"tests"} />
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
    </div>
  );
}
