import React from "react";
import styles from "./RunBatchList.module.scss";
import { Page, PageRequest } from "../../../../components/Pagination/Page";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
import _ from "lodash";
import ErrorMessageBox from "../../../../components/ErrorMessageBox/ErrorMessageBox";
import SimplePaginationControls from "../../../../components/Pagination/SimplePaginationControls";
import { SelectInput } from "../../../../components/Inputs/Select/SelectInput";
import { RunBatchAggregate } from "../../../../catoapimodels/catoapimodels";
import RunBatchListEntry from "./RunBatchListEntry/RunBatchListEntry";
import {
  DataLoadedState,
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "../../../../components/LoadingStateHandler/LoadingStateHandler";
import PlaceHolderText from "../../../../components/PlaceholderText/PlaceHolderText";
import { CollectionHandler } from "../../../../components/CollectionHandler/CollectionHandler";

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
            <th>Created</th>
            <th>Duration</th>
          </tr>
        </thead>
        <tbody>
          <LoadingStateHandler isLoading={props.isLoading} error={props.error}>
            <ErrorState>
              <div className={styles.error}>
                <ErrorMessageBox
                  heading={"An error occurred while loading the runs"}
                  message={props.error?.message}
                />
              </div>
            </ErrorState>
            <LoadingState>
              <SkeletonTheme baseColor="#f7f7f7" highlightColor="white">
                {_.range(7).map((i) => {
                  return (
                    <p key={i}>
                      <Skeleton count={1} width={840} height={60} />
                    </p>
                  );
                })}
              </SkeletonTheme>
            </LoadingState>
            <DataLoadedState>
              <CollectionHandler
                data={props.runs?.entities}
                placeHolder={
                  <div className={"d-flex"}>
                    <PlaceHolderText
                      text={"No runs"}
                      className={styles.noSuitesPlaceholder}
                    />
                  </div>
                }
                renderElements={(data) => {
                  return data.map((runBatch) => {
                    return (
                      <RunBatchListEntry
                        runBatch={runBatch}
                        projectId={props.projectId}
                      />
                    );
                  });
                }}
              />
            </DataLoadedState>
          </LoadingStateHandler>
        </tbody>
      </table>
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
