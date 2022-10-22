import React, { ReactElement } from "react";
import {
  BasicRunInformation,
  RunAggregate,
  RunBatchAggregate,
  RunBatchIdentifier,
} from "../../../../../catoapimodels/catoapimodels";
import ProgressBar from "../../../../../components/ProgressBar/ProgressBar";
import FormattedTime from "../../../../../components/FormattedTime/FormattedTime";
import { formatDuration } from "../../../../../utils/dateUtils";
import RunStatus from "../../../../../components/Status/RunStatus";
import RunInformation from "./RunInformation";
import RunBatchProviderInformation from "./RunBatchProviderInformation";
import Expander from "./Expander";

type RunLike = (RunBatchAggregate | RunAggregate) & {
  runInformation?: BasicRunInformation;
  runBatchIdentifier?: RunBatchIdentifier;
  createdAt?: string;
  startedAt?: string;
};

interface Props {
  isIndented: boolean;
  isExpandable: boolean;
  representsSingleRun: boolean;
  link: ReactElement;
  runLike: RunLike;
  isExpanded: boolean;
  onExpandToggleClick: () => void;
}
/* TODO improve code by using mode
enum Mode {
  EXPENDABLE_RUN_BATCH,
  EXPANDED_RUN_BATCH_ENTRY,
  RUN_BATCH_WITH_SINGLE_RUN,
}*/

function RunBatchListRow(props: Props) {
  const showCaret = props.isExpandable;
  return (
    <tr
      key={props.runLike.id}
      style={props.isExpandable ? { fontWeight: "600" } : {}}
    >
      <td>
        <div className={"d-flex align-items-center"} style={{ gap: "4px" }}>
          {showCaret ? (
            <Expander
              isExpanded={props.isExpanded}
              onExpandToggleClick={props.onExpandToggleClick}
            />
          ) : (
            <div style={{ width: "20x" }} />
          )}
          <div
            className={props.isIndented ? "mr-4" : ""}
            style={{ width: props.isExpandable ? "" : "20px" }}
          />
          {props.link}
          {props.representsSingleRun || props.isExpandable ? (
            <RunBatchProviderInformation
              runBatchProvider={props.runLike.runBatchIdentifier!.provider}
            />
          ) : null}
          {props.runLike.runInformation &&
          (!props.isExpandable || props.representsSingleRun) ? (
            <RunInformation runInformation={props.runLike.runInformation} />
          ) : null}
        </div>
      </td>
      <td>
        <RunStatus status={props.runLike.status} isActive={false} />
      </td>
      <td>
        <ProgressBar
          progressPercentage={props.runLike.progress.progressPercentage}
        />
      </td>
      <td>{props.runLike.branchName}</td>
      <td>
        <FormattedTime
          datestr={props.runLike.createdAt || props.runLike.startedAt}
        />
      </td>
      <td>
        {props.runLike.duration ? formatDuration(props.runLike.duration) : "—"}
      </td>
    </tr>
  );
}

export default RunBatchListRow;