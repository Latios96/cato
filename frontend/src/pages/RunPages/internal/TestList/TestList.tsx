import React from "react";
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
import { FilterOptions } from "../../../../models/FilterOptions";
import { filterOptionsToQueryString } from "../../../../utils/filterOptionUtils";
import { CollectionHandler } from "../../../../components/CollectionHandler/CollectionHandler";
import PlaceHolderText from "../../../../components/PlaceholderText/PlaceHolderText";
import { Thumbnail } from "../../../../components/Thumbnail/Thumbnail";
import { TestResultShortSummaryDto } from "../../../../catoapimodels/catoapimodels";
import { toHoursAndMinutes } from "../../../../utils/dateUtils";

interface Props {
  projectId: number;
  runId: number;
  filterOptions: FilterOptions;
  selectedTestId: number | undefined;
  selectedTestIdChanged: (testId: number) => void;
}

function TestList(props: Props) {
  const url = `/api/v1/test_results/run/${
    props.runId
  }?${filterOptionsToQueryString(props.filterOptions)}`;

  const {
    data: tests,
    isLoading,
    error,
  } = useReFetch<TestResultShortSummaryDto[]>(url, 5000, [
    props.runId,
    props.filterOptions,
  ]);

  return (
    <LoadingStateHandler isLoading={isLoading} error={error}>
      <LoadingState>
        <table className={styles.testList} id={"testList"}>
          <colgroup>
            <col />
            <col />
            <col />
            <col />
            <col />
            <col />
          </colgroup>
          <tbody>
            <SkeletonTheme baseColor="#f7f7f7" highlightColor="white">
              {_.range(25).map((i) => {
                return (
                  <tr>
                    <td>
                      <Skeleton count={1} width={30} height={27} />
                    </td>
                    <td>
                      <Skeleton count={1} width={60} height={30} />
                    </td>
                    <td>
                      <Skeleton count={1} width={150} height={20} />
                    </td>
                    <td>/</td>
                    <td>
                      <Skeleton count={1} width={300} height={20} />
                    </td>
                    <td>
                      <Skeleton count={1} width={35} height={20} />
                    </td>
                  </tr>
                );
              })}
            </SkeletonTheme>
          </tbody>
        </table>
      </LoadingState>
      <ErrorState>
        {" "}
        <ErrorMessageBox
          heading={"An error occurred while loading the test results"}
          message={error?.message}
        />
      </ErrorState>
      <DataLoadedState>
        <table className={styles.testList} id={"testList"}>
          <colgroup>
            <col />
            <col />
            <col />
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
              renderElements={(tests) =>
                tests.map((test) => {
                  return (
                    <tr
                      onClick={() => props.selectedTestIdChanged(test.id)}
                      className={
                        test.id === props.selectedTestId ? styles.active : ""
                      }
                      key={test.id}
                    >
                      <td>
                        <TestStatus testResult={test} />
                      </td>
                      <td>
                        <Thumbnail
                          url={
                            test.thumbnailFileId
                              ? `/api/v1/files/${test.thumbnailFileId}`
                              : undefined
                          }
                          width={"60px"}
                          height={"35px"}
                        />
                      </td>
                      <td>{test.testIdentifier.split("/")[0]}</td>
                      <td>/</td>
                      <td>{test.testIdentifier.split("/")[1]}</td>
                      <td>{toHoursAndMinutes(test.seconds || 0)}</td>
                    </tr>
                  );
                })
              }
            />
          </tbody>
        </table>
      </DataLoadedState>
    </LoadingStateHandler>
  );
}

export default TestList;
