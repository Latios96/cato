import React from "react";
import {
  DataLoadedState,
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "../../../../components/LoadingStateHandler/LoadingStateHandler";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
import _ from "lodash";
import ErrorMessageBox from "../../../../components/ErrorMessageBox/ErrorMessageBox";
import styles from "./SuiteList.module.scss";
import { SuiteListEntry, SuiteListEntrySkeleton } from "./SuiteListEntry";
import { useReFetch } from "../../../../hooks/useReFetch";
import { FilterOptions } from "../../../../models/FilterOptions";
import { filterOptionsToQueryString } from "../../../../utils/filterOptionUtils";
import PlaceHolderText from "../../../../components/PlaceholderText/PlaceHolderText";
import { CollectionHandler } from "../../../../components/CollectionHandler/CollectionHandler";
import { SuiteResultDto } from "../../../../catoapimodels/catoapimodels";
interface Props {
  projectId: number;
  runId: number;
  filterOptions: FilterOptions;
}

function SuiteList(props: Props) {
  const { data, isLoading, error } = useReFetch<SuiteResultDto[]>(
    `/api/v1/suite_results/run/${props.runId}?${filterOptionsToQueryString(
      props.filterOptions
    )}`,
    5000,
    [props.runId, props.filterOptions]
  );

  return (
    <LoadingStateHandler isLoading={isLoading} error={error}>
      <LoadingState>
        <div className={styles.loading}>
          <div className={styles.suiteList} id={"suiteList"}>
            <SkeletonTheme baseColor="#f7f7f7" highlightColor="white">
              {_.range(15).map((i) => {
                return <SuiteListEntrySkeleton />;
              })}
            </SkeletonTheme>
          </div>
        </div>
      </LoadingState>
      <ErrorState>
        <ErrorMessageBox
          heading={"An error occurred while loading the suite results"}
          message={error?.message}
        />
      </ErrorState>
      <DataLoadedState>
        <div className={styles.suiteList} id={"suiteList"}>
          <CollectionHandler
            data={data}
            placeHolder={
              <div className={"d-flex"}>
                <PlaceHolderText
                  text={"No suites"}
                  className={styles.noSuitesPlaceholder}
                />
              </div>
            }
            renderElements={(data) => {
              return data.map((suite) => {
                return (
                  <SuiteListEntry
                    suite={suite}
                    projectId={props.projectId}
                    runId={props.runId}
                  />
                );
              });
            }}
          />
        </div>
      </DataLoadedState>
    </LoadingStateHandler>
  );
}

export default SuiteList;
