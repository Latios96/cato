import React from "react";
import { SuiteResultDto } from "../../../catoapimodels";
import {
  DataLoadedState,
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "../../../components/LoadingStateHandler/LoadingStateHandler";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
import _ from "lodash";
import ErrorMessageBox from "../../../components/ErrorMessageBox/ErrorMessageBox";
import styles from "./SuiteList.module.scss";
import SuiteListEntry from "./SuiteListEntry";
import { useReFetch } from "../../../hooks/useReFetch";
import { useHistory } from "react-router-dom";
import queryString from "query-string";
interface Props {
  projectId: number;
  runId: number;
}

function SuiteList(props: Props) {
  const { data, loading, error } = useReFetch<SuiteResultDto[]>(
    `/api/v1/suite_results/run/${props.runId}`,
    5000,
    [props.runId]
  );
  const history = useHistory();
  const queryParams = queryString.parse(history.location.search, {
    parseNumbers: true,
  });
  // @ts-ignore
  const selectedTestId: number | undefined = queryParams.selectedTest;
  // @ts-ignore
  const selectedSuiteId: number | undefined = queryParams.selectedSuiteId;

  return (
    <LoadingStateHandler isLoading={loading} error={error}>
      <LoadingState>
        <div className={styles.loading}>
          <SkeletonTheme color="#f7f7f7" highlightColor="white">
            {_.range(10).map((i) => {
              return (
                <p>
                  <Skeleton count={1} width={720} height={40} />
                </p>
              );
            })}
          </SkeletonTheme>
        </div>
      </LoadingState>
      <ErrorState>
        {" "}
        <ErrorMessageBox
          heading={"Error when loading run summary"}
          message={error?.message}
        />
      </ErrorState>
      <DataLoadedState>
        <div className={styles.suiteList}>
          {data
            ? data.map((suite) => {
                return (
                  <SuiteListEntry
                    suite={suite}
                    projectId={props.projectId}
                    runId={props.runId}
                    testSelected={(suiteId, testId) => {
                      history.push(
                        `/projects/${props.projectId}/runs/${props.runId}/suites/?selectedTest=${testId}&selectedSuiteId=${suiteId}`
                      );
                    }}
                    selectedTestId={selectedTestId}
                    expand={selectedSuiteId === suite.id}
                  />
                );
              })
            : ""}
        </div>
      </DataLoadedState>
    </LoadingStateHandler>
  );
}

export default SuiteList;
