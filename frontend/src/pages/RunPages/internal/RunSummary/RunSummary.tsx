import InfoBox from "../../../../components/InfoBox/InfoBox";
import InfoBoxElement from "../../../../components/InfoBox/InfoBoxElement/InfoBoxElement";
import { formatDuration } from "../../../../utils/dateUtils";
import React from "react";

import styles from "./RunSummary.module.scss";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
import {
  DataLoadedState,
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "../../../../components/LoadingStateHandler/LoadingStateHandler";
import ErrorMessageBox from "../../../../components/ErrorMessageBox/ErrorMessageBox";
import { useReFetch } from "../../../../hooks/useReFetch";
import UnsyncedEdits from "../../../../components/UnsyncedEdits/UnsyncedEdits";
import { calculateStatusPercentage } from "./utils";
import { RunSummaryProgressBar } from "./RunSummaryProgressBar";
import {
  RunSummaryDto,
  TestEditCount,
} from "../../../../catoapimodels/catoapimodels";

interface Props {
  runId: number;
}

export function RunSummary(props: Props) {
  const {
    data: runSummaryDto,
    isLoading,
    error,
  } = useReFetch<RunSummaryDto>(`/api/v1/runs/${props.runId}/summary`, 5000, [
    props.runId,
  ]);

  const {
    data: editsToSync,
    isLoading: editsToSyncLoading,
    error: editsToSyncError,
  } = useReFetch<TestEditCount>(
    `/api/v1/test_edits/runs/${props.runId}/edits-to-sync-count`,
    5000,
    [props.runId]
  );

  function renderSummary(runSummaryDto: RunSummaryDto) {
    const statusPercentage = calculateStatusPercentage(runSummaryDto);
    return (
      <>
        <InfoBox>
          <InfoBoxElement
            value={"" + runSummaryDto.suiteCount}
            title={"suites"}
            id={"runSummary suites"}
          />
          <InfoBoxElement
            value={"" + runSummaryDto.testCount}
            title={"tests"}
            id={"runSummary tests"}
          />
          <InfoBoxElement
            value={"" + runSummaryDto.failedTestCount}
            title={"failed tests"}
            id={"runSummary failed tests"}
          />
          <InfoBoxElement
            value={
              "" +
              formatDuration(
                runSummaryDto.run.duration ? runSummaryDto.run.duration : 0
              )
            }
            title={"duration"}
            id={"runSummary duration"}
          />
        </InfoBox>
        <RunSummaryProgressBar statusPercentage={statusPercentage} />
      </>
    );
  }

  return (
    <div className={styles.runSummary}>
      <LoadingStateHandler isLoading={isLoading} error={error}>
        <LoadingState>
          <SkeletonTheme color="#f7f7f7" highlightColor="white">
            <p>
              <Skeleton count={1} width={720} height={100} />
            </p>
            <p>
              <Skeleton count={1} width={720} height={25} />
            </p>
          </SkeletonTheme>
        </LoadingState>
        <ErrorState>
          <ErrorMessageBox
            heading={"An error occurred while loading the run summary"}
            message={error?.message}
          />
        </ErrorState>
        <DataLoadedState>
          {runSummaryDto ? renderSummary(runSummaryDto) : null}
        </DataLoadedState>
      </LoadingStateHandler>
      <LoadingStateHandler
        isLoading={editsToSyncLoading}
        error={editsToSyncError}
      >
        <DataLoadedState>
          {editsToSync && editsToSync.count ? (
            <UnsyncedEdits
              runId={props.runId}
              unsyncedEditCount={editsToSync ? editsToSync.count : 0}
            />
          ) : (
            <></>
          )}
        </DataLoadedState>
      </LoadingStateHandler>
    </div>
  );
}
