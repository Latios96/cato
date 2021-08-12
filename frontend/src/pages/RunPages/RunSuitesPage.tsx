import React from "react";
import BasicRunPage from "./internal/common/BasicRunPage";
import { CurrentPage } from "./internal/common/CurrentPage";
import styles from "./RunTestsPage.module.scss";
import TestResultComponent from "../../components/TestResultComponent/TestResultComponent";
import PlaceHolderText from "../../components/PlaceholderText/PlaceHolderText";
import { useLocation } from "react-router-dom";
import queryString from "query-string";
import SuiteList from "./internal/SuiteList/SuiteList";
interface Props {
  projectId: number;
  runId: number;
}

function RunSuitePage(props: Props) {
  const location = useLocation();
  const queryParams = queryString.parse(location.search, {
    parseNumbers: true,
  });
  // @ts-ignore
  const selectedTestId: number = queryParams.selectedTest;
  return (
    <BasicRunPage {...props} currentPage={CurrentPage.SUITES}>
      <div className={styles.suiteAndTestContainer}>
        <div>
          <SuiteList projectId={props.projectId} runId={props.runId} />
        </div>
        <div>
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

export default RunSuitePage;
