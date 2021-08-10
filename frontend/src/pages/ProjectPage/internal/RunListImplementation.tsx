import React from "react";
import styles from "./RunList.module.scss";
import RunStatus from "../../../components/Status/RunStatus";
import { Link } from "react-router-dom";
import { formatDuration, formatTime } from "../../../utils";
import { RunDto } from "../../../catoapimodels";
import { Page, PageRequest } from "../../../components/Pagination/Page";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
import _ from "lodash";
import ErrorMessageBox from "../../../components/ErrorMessageBox/ErrorMessageBox";
import SimplePaginationControls from "../../../components/Pagination/SimplePaginationControls";

interface Props {
  projectId: number;
  runs: Page<RunDto> | undefined;
  isLoading: boolean;
  error?: Error;
  pageChangedCallback: (pageRequest: PageRequest) => void;
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
      <table id={"runList"}>
        <colgroup>
          <col />
          <col />
          <col />
          <col />
        </colgroup>
        <thead>
          <tr>
            <th>Status</th>
            <th>Run</th>
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
                    <td>{formatTime(run.started_at)}</td>
                    <td>{formatDuration(10)}</td>
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
