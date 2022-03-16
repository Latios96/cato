import styles from "./SuiteListEntry.module.scss";
import {
  DataLoadedState,
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "../../../../components/LoadingStateHandler/LoadingStateHandler";
import ErrorMessageBox from "../../../../components/ErrorMessageBox/ErrorMessageBox";
import Skeleton from "react-loading-skeleton";
import TestStatus from "../../../../components/Status/TestStatus";
import React from "react";
import { Thumbnail } from "../../../../components/Thumbnail/Thumbnail";
import { TestResultDto } from "../../../../catoapimodels/catoapimodels";
interface Props {
  loading: boolean;
  error?: Error;
  data: TestResultDto[] | undefined;
  onClick: (test: TestResultDto) => void;
  selectedTestId: any;
  suiteId: number;
}

export function SuiteTestListImpl(props: Props) {
  return (
    <div
      className={styles.suiteListEntryContent}
      id={`suiteListEntryContent${props.suiteId}`}
    >
      <LoadingStateHandler isLoading={props.loading}>
        <ErrorState>
          <ErrorMessageBox
            heading={"An error occurred while loading the tests"}
            message={props.error?.message}
          />
        </ErrorState>
        <LoadingState>
          <div>
            <Skeleton count={1} width={250} height={20} />
          </div>
          <div>
            <Skeleton count={1} width={250} height={20} />
          </div>
          <div>
            <Skeleton count={1} width={250} height={20} />
          </div>
        </LoadingState>
        <DataLoadedState>
          {props.data ? (
            <>
              {props.data.length === 0 ? (
                <div>
                  <span>This suite has no tests</span>
                </div>
              ) : null}
              {props.data.map((test) => {
                return (
                  <div
                    onClick={() => props.onClick(test)}
                    className={
                      props.selectedTestId === test.id ? styles.active : ""
                    }
                    id={`suite-${props.suiteId}-test-${test.id}`}
                  >
                    <span>
                      <TestStatus testResult={test} />
                    </span>
                    <span>
                      <Thumbnail
                        url={
                          test.thumbnail_file_id
                            ? `/api/v1/files/${test.thumbnail_file_id}`
                            : undefined
                        }
                        width={"55px"}
                        height={"30px"}
                      />
                    </span>
                    <span>{test.test_name}</span>
                  </div>
                );
              })}
            </>
          ) : null}
        </DataLoadedState>
      </LoadingStateHandler>
    </div>
  );
}
