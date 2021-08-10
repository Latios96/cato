import React from "react";
import { TestResultShortSummaryDto } from "../../../catoapimodels";
import styles from "./TestList.module.scss";
import { useHistory, useLocation } from "react-router-dom";
import queryString from "query-string";
import TestStatus from "../../../components/Status/TestStatus";
import { useReFetch } from "../../../hooks/useReFetch";
import _ from "lodash";
import {
  DataLoadedState,
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "../../../components/LoadingStateHandler/LoadingStateHandler";
import ErrorMessageBox from "../../../components/ErrorMessageBox/ErrorMessageBox";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
interface Props {
  projectId: number;
  runId: number;
}

function TestList(props: Props) {
  const {
    data: tests,
    loading,
    error,
  } = useReFetch<TestResultShortSummaryDto[]>(
    `/api/v1/test_results/run/${props.runId}`,
    5000,
    [props.runId]
  );

  const history = useHistory();
  const location = useLocation();
  const queryParams = queryString.parse(location.search, {
    parseNumbers: true,
  });
  const selectedTestId = queryParams.selectedTest;
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
        <table className={styles.testList}>
          <colgroup>
            <col />
            <col />
            <col />
          </colgroup>
          <tbody>
            {tests
              ? _.sortBy(tests, "test_identifier").map((test) => {
                  return (
                    <tr
                      onClick={() =>
                        history.push(
                          `/projects/${props.projectId}/runs/${props.runId}/tests/?selectedTest=${test.id}`
                        )
                      }
                      className={
                        test.id === selectedTestId ? styles.active : ""
                      }
                    >
                      <td>
                        <TestStatus testResult={test} />
                      </td>
                      <td>{test.test_identifier.split("/")[0]}</td>
                      <td>/</td>
                      <td>{test.test_identifier.split("/")[1]}</td>
                    </tr>
                  );
                })
              : null}
          </tbody>
        </table>
      </DataLoadedState>
    </LoadingStateHandler>
  );
}

export default TestList;
