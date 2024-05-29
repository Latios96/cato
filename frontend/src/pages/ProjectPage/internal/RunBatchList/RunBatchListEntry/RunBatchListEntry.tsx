import React from "react";
import { RunBatchAggregate } from "../../../../../catoapimodels/catoapimodels";
import RunBatchListRow, { RunLike } from "./RunBatchListRow";
import { Link } from "react-router-dom";
import { useToggle } from "rooks";

interface Props {
  runBatch: RunBatchAggregate;
  projectId: number;
}

function RunBatchListEntry(props: Props) {
  const [isExpanded, toggleExpanded] = useToggle(false);
  const hasSingleRun = props.runBatch.runs.length === 1;

  let runLike: RunLike = props.runBatch;
  if (hasSingleRun) {
    runLike = {
      runInformation: props.runBatch.runs[0].runInformation,
      runBatchIdentifier: props.runBatch.runBatchIdentifier,
      createdAt: props.runBatch.runs[0].createdAt,
      status: props.runBatch.runs[0].status,
      branchName: props.runBatch.runs[0].branchName,
      duration: props.runBatch.runs[0].duration,
      id: props.runBatch.runs[0].id,
      progress: props.runBatch.progress,
    };
  } else {
    runLike.duration = props.runBatch.runs.reduce(
      (duration, aggregate) => duration + aggregate.duration,
      0
    );
  }

  return (
    <>
      <RunBatchListRow
        key={props.runBatch.id}
        isExpandable={!hasSingleRun}
        isExpanded={isExpanded}
        isIndented={false}
        representsSingleRun={hasSingleRun}
        onExpandToggleClick={() => toggleExpanded(!isExpanded)}
        label={
          hasSingleRun ? (
            <Link
              to={`/projects/${props.projectId}/runs/${props.runBatch.runs[0].id}`}
            >
              {"#" + props.runBatch.runs[0].id}
            </Link>
          ) : (
            <>{props.runBatch.runBatchIdentifier.runName}</>
          )
        }
        runLike={runLike}
      />
      {props.runBatch.runs.length > 1 && isExpanded
        ? props.runBatch.runs.map((run) => {
            return (
              <RunBatchListRow
                key={run.id}
                isIndented={true}
                isExpandable={false}
                isExpanded={false}
                representsSingleRun={false}
                onExpandToggleClick={() => {}}
                label={
                  <Link to={`/projects/${props.projectId}/runs/${run.id}`}>
                    {"#" + run.id}
                  </Link>
                }
                runLike={run}
              />
            );
          })
        : null}
    </>
  );
}

export default RunBatchListEntry;
