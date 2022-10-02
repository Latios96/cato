import React, { ReactElement } from "react";
import {
  BasicRunInformation,
  RunBatchIdentifier,
  RunProgress,
  RunStatus as RunStatusEnum,
} from "../../../../catoapimodels/catoapimodels";
import { CaretRightFill } from "react-bootstrap-icons";
import ProgressBar from "./ProgressBar";
import FormattedTime from "../../../../components/FormattedTime/FormattedTime";
import { formatDuration } from "../../../../utils/dateUtils";
import RunStatus from "../../../../components/Status/RunStatus";
import RunInformation from "./RunInformation";

interface Props {
  id: number;
  isIndented: boolean;
  isExpandable: boolean;
  link: ReactElement;
  runBatchIdentifier: RunBatchIdentifier;
  status: RunStatusEnum;
  branchName: string;
  createdAt: string;
  duration: number;
  progress: RunProgress;
  runInformation?: BasicRunInformation;
}

function RunBatchListRow(props: Props) {
  const showCaret = props.isExpandable;
  return (
    <tr key={props.id}>
      <td>
        <div className={"d-flex align-items-center"}>
          {showCaret ? (
            <CaretRightFill size={16} />
          ) : (
            <div style={{ width: "16px" }} />
          )}
          {props.isIndented ? <div style={{ width: "25px" }} /> : null}
          {props.link}
          {props.runInformation ? (
            <RunInformation runInformation={props.runInformation} />
          ) : null}
        </div>
      </td>
      <td>
        <RunStatus status={props.status} isActive={false} />
      </td>
      <td>
        <ProgressBar progressPercentage={props.progress.progressPercentage} />
      </td>
      <td>{props.branchName}</td>
      <td>
        <FormattedTime datestr={props.createdAt} />
      </td>
      <td>{props.duration ? formatDuration(props.duration) : "—"}</td>
    </tr>
  );
}

export default RunBatchListRow;
