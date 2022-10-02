import React from "react";
import styles from "./RunBatchList.module.scss";
import { Link } from "react-router-dom";
import { Page, PageRequest } from "../../../../components/Pagination/Page";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
import _ from "lodash";
import ErrorMessageBox from "../../../../components/ErrorMessageBox/ErrorMessageBox";
import SimplePaginationControls from "../../../../components/Pagination/SimplePaginationControls";
import { SelectInput } from "../../../../components/Inputs/Select/SelectInput";
import { RunBatchAggregate } from "../../../../catoapimodels/catoapimodels";
import RunBatchListRow from "./RunBatchListRow";

interface Props {
  projectId: number;
  runs: Page<RunBatchAggregate> | undefined;
  isLoading: boolean;
  error?: Error;
  pageChanged: (pageRequest: PageRequest) => void;
  filteredBranchesChanged: (branches: Set<string>) => void;
  branches: string[];
  selectedBranches: Set<string>;
}

function RunBatchListImplementation(props: Props) {
  if (props.error) {
    return (
      <div className={styles.error}>
        <ErrorMessageBox
          heading={"An error occurred while loading the runs"}
          message={props.error.message}
        />
      </div>
    );
  }

  return (
    <div className={styles.runList}>
      <div className={styles.branchSelectorContainer}>
        <SelectInput
          id={"branchSelector"}
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
          <col />
        </colgroup>
        <thead>
          <tr>
            <th>Run</th>
            <th>Status</th>
            <th>Progress</th>
            <th>Branch</th>
            <th>Started</th>
            <th>Duration</th>
          </tr>
        </thead>
        <tbody>
          {props.runs && !props.isLoading
            ? props.runs.entities.map((runBatch) => {
                const hasSingleRun = runBatch.runs.length <= 1;
                return (
                  <>
                    <RunBatchListRow
                      key={runBatch.id}
                      id={runBatch.id}
                      isExpandable={!hasSingleRun}
                      isIndented={false}
                      link={
                        hasSingleRun ? (
                          <Link
                            to={`/projects/${props.projectId}/runs/${runBatch.id}`}
                          >
                            {"#" + runBatch.id}
                          </Link>
                        ) : (
                          <>{"#" + runBatch.id}</>
                        )
                      }
                      runBatchIdentifier={runBatch.runBatchIdentifier}
                      status={runBatch.status}
                      progress={runBatch.progress}
                      branchName={runBatch.branchName}
                      createdAt={runBatch.createdAt}
                      duration={runBatch.duration}
                    />
                    {runBatch.runs.length > 1
                      ? runBatch.runs.map((run) => {
                          return (
                            <RunBatchListRow
                              id={run.id}
                              key={run.id}
                              isIndented={true}
                              isExpandable={false}
                              link={
                                <Link
                                  to={`/projects/${props.projectId}/runs/${run.id}`}
                                >
                                  {"#" + run.id}
                                </Link>
                              }
                              runBatchIdentifier={runBatch.runBatchIdentifier}
                              status={run.status}
                              progress={run.progress}
                              branchName={run.branchName}
                              createdAt={run.startedAt}
                              duration={run.duration}
                              runInformation={run.runInformation}
                            />
                          );
                        })
                      : null}
                  </>
                );
              })
            : null}
        </tbody>
      </table>
      {props.isLoading ? (
        <SkeletonTheme baseColor="#f7f7f7" highlightColor="white">
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
            pageChangedCallback={props.pageChanged}
          />
        </div>
      ) : null}
    </div>
  );
}

export default RunBatchListImplementation;
