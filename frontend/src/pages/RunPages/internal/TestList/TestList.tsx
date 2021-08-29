import React from "react";
import { TestResultShortSummaryDto } from "../../../../catoapimodels";
import styles from "./TestList.module.scss";
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
import { TestResultFilterOptions } from "../../../../models/TestResultFilterOptions";
import { testResultFilterOptionsToQueryString } from "../../../../utils/filterOptionUtils";
import { CollectionHandler } from "../../../../components/CollectionHandler/CollectionHandler";
import PlaceHolderText from "../../../../components/PlaceholderText/PlaceHolderText";
interface Props {
  projectId: number;
  runId: number;
  testResultFilterOptions: TestResultFilterOptions;
  selectedTestId: number | undefined;
  selectedTestIdChanged: (testId: number) => void;
}

function TestList(props: Props) {
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
            <CollectionHandler
              data={tests}
              placeHolder={
                <div className={"d-flex"}>
                  <PlaceHolderText
                    text={"No tests"}
                    className={styles.noTestPlaceholder}
                  />
                </div>
              }
              renderDataElement={(test) => {
                return (
                  <tr
                    onClick={() => props.selectedTestIdChanged(test.id)}
                    className={
                      test.id === props.selectedTestId ? styles.active : ""
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
              }}
            />
          </tbody>
        </table>
      </DataLoadedState>
    </LoadingStateHandler>
  );
}

export default TestList;
