import { RunSummaryDto } from "../../../catoapimodels";
import InfoBox from "../../../components/InfoBox/InfoBox";
import InfoBoxElement from "../../../components/InfoBox/InfoBoxElement/InfoBoxElement";
import { formatDuration } from "../../../utils";
import React from "react";

import styles from "./RunSummary.module.scss";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
import {
  DataLoadedState,
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "../../../components/LoadingStateHandler/LoadingStateHandler";
import ErrorMessageBox from "../../../components/ErrorMessageBox/ErrorMessageBox";
import { useReFetch } from "../../../useReFetch";
interface Props {
  runId: number;
}
export function RunSummary(props: Props) {
  const {
    data: runSummaryDto,
    loading,
    error,
  } = useReFetch(`/api/v1/runs/${props.runId}/summary`, 5000, [props.runId]);

  return (
    <div className={styles.runSummary}>
      <LoadingStateHandler isLoading={loading} error={error}>
        <LoadingState>
          <SkeletonTheme color="#f7f7f7" highlightColor="white">
            <p>
              <Skeleton count={1} width={720} height={100} />
            </p>
          </SkeletonTheme>
        </LoadingState>
        <ErrorState>
          <ErrorMessageBox
            heading={"Error when loading run summary"}
            message={error?.message}
          />
        </ErrorState>
        <DataLoadedState>
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
                    runSummaryDto.duration !== "NaN"
                      ? runSummaryDto.duration
                      : 0
                  )
                }
                title={"duration"}
              />
            </InfoBox>
          ) : null}
        </DataLoadedState>
      </LoadingStateHandler>
    </div>
  );
}
