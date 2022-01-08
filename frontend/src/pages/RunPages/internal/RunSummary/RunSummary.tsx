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
import { TestEditCount } from "../../../../models/TestEditCount";
import { calculateStatusPercentage } from "./utils";
import { RunSummaryProgressBar } from "./RunSummaryProgressBar";

interface Props {
  runId: number;
}

export function RunSummary(props: Props) {
  const {
    data: runSummaryDto,
    isLoading,
    error,
  } = useReFetch(`/api/v1/runs/${props.runId}/summary`, 5000, [props.runId]);

  const {
    data: editsToSync,
    isLoading: editsToSyncLoading,
    error: editsToSyncError,
  } = useReFetch<TestEditCount>(
    `/api/v1/test_edits/runs/${props.runId}/edits-to-sync-count`,
    5000,
    [props.runId]
  );

  function renderSummary() {
    const statusPercentage = calculateStatusPercentage(runSummaryDto);
    return (
      <>
        <InfoBox>
          <InfoBoxElement
            value={"" + runSummaryDto.suite_count}
            title={"suites"}
            id={"runSummary suites"}
          />
          <InfoBoxElement
            value={"" + runSummaryDto.test_count}
            title={"tests"}
            id={"runSummary tests"}
          />
          <InfoBoxElement
            value={"" + runSummaryDto.failed_test_count}
            title={"failed tests"}
            id={"runSummary failed tests"}
          />
          <InfoBoxElement
            value={
              "" +
              formatDuration(
                runSummaryDto.run.duration !== "NaN"
                  ? runSummaryDto.run.duration
                  : 0
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
            heading={"Error when loading run summary"}
            message={error?.message}
          />
        </ErrorState>
        <DataLoadedState>
          {runSummaryDto ? renderSummary() : null}
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
