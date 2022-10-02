import React from "react";
import { RunBatchAggregate } from "../../../../catoapimodels/catoapimodels";
import RunBatchListRow from "./RunBatchListRow";
import { Link } from "react-router-dom";
import { useToggle } from "rooks";

interface Props {
  runBatch: RunBatchAggregate;
  projectId: number;
}

function RunBatchListEntry(props: Props) {
  const [isExpanded, toggleExpanded] = useToggle(false);
  const hasSingleRun = props.runBatch.runs.length === 1;
  return (
    <>
      <RunBatchListRow
        key={props.runBatch.id}
        isExpandable={!hasSingleRun}
        isExpanded={isExpanded}
        isIndented={false}
        representsSingleRun={hasSingleRun}
        onExpandToggleClick={() => toggleExpanded(!isExpanded)}
        link={
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
        runLike={{ ...props.runBatch, ...props.runBatch.runs[0] }}
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
                link={
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
