import React from "react";
import { RunBatchAggregate } from "../../../../catoapimodels/catoapimodels";
import RunBatchListRow from "./RunBatchListRow";
import { Link } from "react-router-dom";

interface Props {
  runBatch: RunBatchAggregate;
  projectId: number;
}

function RunBatchListEntry(props: Props) {
  const hasSingleRun = props.runBatch.runs.length === 1;
  return (
    <>
      <RunBatchListRow
        key={props.runBatch.id}
        isExpandable={!hasSingleRun}
        isIndented={false}
        representsSingleRun={hasSingleRun}
        link={
          hasSingleRun ? (
            <Link
              to={`/projects/${props.projectId}/runs/${props.runBatch.runs[0].id}`}
            >
              {"#" + props.runBatch.id}
            </Link>
          ) : (
            <>{"#" + props.runBatch.id}</>
          )
        }
        runLike={{ ...props.runBatch, ...props.runBatch.runs[0] }}
      />
      {props.runBatch.runs.length > 1
        ? props.runBatch.runs.map((run) => {
            return (
              <RunBatchListRow
                key={run.id}
                isIndented={true}
                isExpandable={false}
                representsSingleRun={false}
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
