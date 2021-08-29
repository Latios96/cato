import React from "react";
import { TestResultShortSummaryDto } from "../../../../catoapimodels";
import styles from "./TestList.module.scss";
import { useHistory } from "react-router-dom";
import queryString from "query-string";
import TestStatus from "../../../../components/Status/TestStatus";
import { useReFetch } from "../../../../hooks/useReFetch";
import _ from "lodash";
import {
  DataLoadedState,
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "../../../../components/LoadingStateHandler/LoadingStateHandler";
import ErrorMessageBox from "../../../../components/ErrorMessageBox/ErrorMessageBox";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
import { updateQueryString } from "../../../../utils/queryStringUtils";
import { TestResultFilterOptions } from "../../../../models/TestResultFilterOptions";
import { testResultFilterOptionsToQueryString } from "../../../../utils/filterOptionUtils";
interface Props {
  projectId: number;
  runId: number;
  testResultFilterOptions: TestResultFilterOptions;
}

function TestList(props: Props) {
  // todo refactor this, list state up
  const history = useHistory();
  const queryParams = queryString.parse(history.location.search, {
    parseNumbers: true,
  });
  const url = `/api/v1/test_results/run/${
    props.runId
  }?${testResultFilterOptionsToQueryString(props.testResultFilterOptions)}`;
  const {
    data: tests,
    loading,
    error,
  } = useReFetch<TestResultShortSummaryDto[]>(url, 5000, [
    props.runId,
    props.testResultFilterOptions,
  ]);

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
        <table className={styles.testList} id={"testList"}>
          <colgroup>
            <col />
            <col />
            <col />
          </colgroup>
          <tbody>
            {
              tests
                ? tests.map((test) => {
                    return (
                      <tr
                        onClick={() =>
                          history.push({
                            search: updateQueryString(history.location.search, {
                              selectedTest: test.id,
                            }),
                          })
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
                : null /* todo display "no tests"*/
            }
          </tbody>
        </table>
      </DataLoadedState>
    </LoadingStateHandler>
  );
}

export default TestList;
