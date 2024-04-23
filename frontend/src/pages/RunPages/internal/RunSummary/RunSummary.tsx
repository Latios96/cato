import InfoBox from "../../../../components/InfoBox/InfoBox";
import InfoBoxElement from "../../../../components/InfoBox/InfoBoxElement/InfoBoxElement";
import { formatDuration } from "../../../../utils/dateUtils";
import React from "react";

import styles from "./RunSummary.module.scss";
import Skeleton from "react-loading-skeleton";
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
  RunAggregate,
  TestEditCount,
} from "../../../../catoapimodels/catoapimodels";
import PerformanceTraceButton from "../../../../components/PerformanceTraceButton/PerformanceTraceButton";
import { Speedometer2 } from "react-bootstrap-icons";

interface Props {
  runId: number;
}

export function RunSummary(props: Props) {
  const {
    data: runAggregate,
    isLoading,
    error,
  } = useReFetch<RunAggregate>(`/api/v1/runs/${props.runId}/aggregate`, 5000, [
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

  function renderSummary(runAggregate: RunAggregate) {
    const statusPercentage = calculateStatusPercentage(runAggregate);
    return (
      <>
        <InfoBox>
          <InfoBoxElement
            value={"" + runAggregate.suiteCount}
            title={"suites"}
            id={"runSummary suites"}
          />
          <InfoBoxElement
            value={"" + runAggregate.testCount}
            title={"tests"}
            id={"runSummary tests"}
          />
          <InfoBoxElement
            value={"" + runAggregate.progress.failedTestCount}
            title={"failed tests"}
            id={"runSummary failed tests"}
          />
          <InfoBoxElement
            value={
              "" +
              formatDuration(runAggregate.duration ? runAggregate.duration : 0)
            }
            title={"duration"}
            id={"runSummary duration"}
          />
        </InfoBox>
        <RunSummaryProgressBar statusPercentage={statusPercentage} />
        {runAggregate.performanceTraceId != null ? (
          <div className={"flex"}>
            <Speedometer2 size={16} className={"m-1"} />
            <span className={"m-1"}>Cato Client Performance Trace</span>
            <PerformanceTraceButton
              runId={runAggregate.id}
              performanceTraceId={runAggregate.performanceTraceId}
            >
              Open
            </PerformanceTraceButton>
          </div>
        ) : null}
      </>
    );
  }

  return (
    <div className={styles.runSummary}>
      <LoadingStateHandler isLoading={isLoading} error={error}>
        <LoadingState>
          <p>
            <Skeleton count={1} width={720} height={100} />
          </p>
          <p>
            <Skeleton count={1} width={720} height={25} />
          </p>
        </LoadingState>
        <ErrorState>
          <ErrorMessageBox
            heading={"An error occurred while loading the run summary"}
            message={error?.message}
          />
        </ErrorState>
        <DataLoadedState>
          {runAggregate ? renderSummary(runAggregate) : null}
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
