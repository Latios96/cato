import React from "react";
import BasicRunPage from "./internal/BasicRunPage";
import { CurrentPage } from "./internal/CurrentPage";
import styles from "./RunTestsPage.module.scss";
import TestList from "./internal/TestList";
import { useLocation } from "react-router-dom";
import queryString from "query-string";
import TestResultComponent from "../../components/TestResultComponent/TestResultComponent";
import PlaceHolderText from "../../components/PlaceholderText/PlaceHolderText";
interface Props {
  projectId: number;
  runId: number;
}

function RunTestsPage(props: Props) {
  const location = useLocation();
  const queryParams = queryString.parse(location.search, {
    parseNumbers: true,
  });
  // @ts-ignore
  const selectedTestId: number = queryParams.selectedTest;

  return (
    <BasicRunPage {...props} currentPage={CurrentPage.TESTS}>
      <div className={styles.suiteAndTestContainer}>
        <div>
          <TestList projectId={props.projectId} runId={props.runId} />
        </div>
        <div id={"selectedTestContainer"}>
          <div>
            {selectedTestId ? (
              <TestResultComponent
                runId={props.runId}
                projectId={props.projectId}
                resultId={selectedTestId}
              />
            ) : (
              <div className={styles.noTestSelected}>
                <PlaceHolderText
                  text={"No test selected"}
                  className={styles.centered}
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </BasicRunPage>
  );
}

export default RunTestsPage;
