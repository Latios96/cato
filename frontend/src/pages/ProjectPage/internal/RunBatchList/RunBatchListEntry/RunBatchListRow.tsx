import React, { ReactElement } from "react";
import {
  BasicRunInformation,
  RunBatchIdentifier,
  RunProgress,
  RunStatus as RunStatus_,
} from "../../../../../catoapimodels/catoapimodels";
import ProgressBar from "../../../../../components/ProgressBar/ProgressBar";
import FormattedTime from "../../../../../components/FormattedTime/FormattedTime";
import { toHoursAndMinutes } from "../../../../../utils/dateUtils";
import RunStatus from "../../../../../components/Status/RunStatus";
import RunInformation from "./RunInformation";
import RunBatchProviderInformation from "./RunBatchProviderInformation";
import Expander from "./Expander";
import styles from "./RunBatchListRow.module.scss";

export interface RunLike {
  runInformation?: BasicRunInformation;
  runBatchIdentifier?: RunBatchIdentifier;
  createdAt?: string;
  status: RunStatus_;
  branchName: string;
  duration: number;
  id: number;
  progress: RunProgress;
}

interface Props {
  isIndented: boolean;
  isExpandable: boolean;
  representsSingleRun: boolean;
  label: ReactElement;
  runLike: RunLike;
  isExpanded: boolean;
  onExpandToggleClick: () => void;
}

function RunBatchListRow(props: Props) {
  const showCaret = props.isExpandable;

  function renderCarret() {
    return (
      <>
        {showCaret ? (
          <Expander
            isExpanded={props.isExpanded}
            onExpandToggleClick={props.onExpandToggleClick}
          />
        ) : null}
      </>
    );
  }

  function renderRunBatchProviderInformation() {
    return (
      <>
        {props.representsSingleRun || props.isExpandable ? (
          <RunBatchProviderInformation
            runBatchProvider={props.runLike.runBatchIdentifier!.provider}
          />
        ) : null}
      </>
    );
  }

  function renderRunInformation() {
    return (
      <>
        {props.runLike.runInformation && !props.isExpandable ? (
          <RunInformation runInformation={props.runLike.runInformation} />
        ) : null}
      </>
    );
  }

  return (
    <tr
      key={props.runLike.id}
      className={props.isExpandable ? styles.boldRow : ""}
    >
      <td>
        <div className={styles.row}>
          {renderCarret()}
          <div
            className={`${props.isIndented ? "mr-4" : ""} ${
              !props.isExpandable ? styles.indenter : ""
            }`}
          />
          {props.label}
          {renderRunBatchProviderInformation()}
          {renderRunInformation()}
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
        <FormattedTime datestr={props.runLike.createdAt} />
      </td>
      <td>
        {props.runLike.duration
          ? toHoursAndMinutes(props.runLike.duration)
          : "—"}
      </td>
    </tr>
  );
}

export default RunBatchListRow;
