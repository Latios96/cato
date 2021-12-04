import React from "react";
import styles from "./RunList.module.scss";
import RunStatus from "../../../components/Status/RunStatus";
import { Link } from "react-router-dom";
import { formatDuration, formatTime } from "../../../utils/dateUtils";
import { RunDto } from "../../../catoapimodels";
import { Page, PageRequest } from "../../../components/Pagination/Page";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
import _ from "lodash";
import ErrorMessageBox from "../../../components/ErrorMessageBox/ErrorMessageBox";
import SimplePaginationControls from "../../../components/Pagination/SimplePaginationControls";
import { SelectInput } from "../../../components/Inputs/Select/SelectInput";

interface Props {
  projectId: number;
  runs: Page<RunDto> | undefined;
  isLoading: boolean;
  error?: Error;
  pageChangedCallback: (pageRequest: PageRequest) => void;
  filteredBranchesChanged: (branches: Set<string>) => void;
  branches: string[];
  selectedBranches: Set<string>;
}

function RunListImplementation(props: Props) {
  if (props.error) {
    return (
      <div className={styles.error}>
        <ErrorMessageBox
          heading={"Error when loading runs"}
          message={props.error.message}
        />
      </div>
    );
  }

  return (
    <div className={styles.runList}>
      <div className={styles.branchSelectorContainer}>
        <SelectInput
          title={"Branch"}
          subtitle={"Filter by branch"}
          elements={props.branches}
          onChange={props.filteredBranchesChanged}
          selectedElements={props.selectedBranches}
        />
      </div>
      <table id={"runList"}>
        <colgroup>
          <col />
          <col />
          <col />
          <col />
          <col />
        </colgroup>
        <thead>
          <tr>
            <th>Status</th>
            <th>Run</th>
            <th>Branch</th>
            <th>Started</th>
            <th>Duration</th>
          </tr>
        </thead>
        <tbody>
          {props.runs && !props.isLoading
            ? props.runs.entities.map((run) => {
                return (
                  <tr key={run.id}>
                    <td>
                      <RunStatus status={run.status} isActive={false} />
                    </td>
                    <td>
                      <Link to={`/projects/${props.projectId}/runs/${run.id}`}>
                        {"Run #" + run.id}
                      </Link>
                    </td>
                    <td>{run.branch_name}</td>
                    <td>{formatTime(run.started_at)}</td>
                    <td>{run.duration ? formatDuration(run.duration) : "—"}</td>
                  </tr>
                );
              })
            : null}
        </tbody>
      </table>
      {props.isLoading ? (
        <SkeletonTheme color="#f7f7f7" highlightColor="white">
          {_.range(7).map((i) => {
            return (
              <p key={i}>
                <Skeleton count={1} width={840} height={60} />
              </p>
            );
          })}
        </SkeletonTheme>
      ) : null}
      {props.runs ? (
        <div className={styles.paginationControls}>
          <SimplePaginationControls
            currentPage={props.runs}
            pageChangedCallback={props.pageChangedCallback}
          />
        </div>
      ) : null}
    </div>
  );
}

export default RunListImplementation;
