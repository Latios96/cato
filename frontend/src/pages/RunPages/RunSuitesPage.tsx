import React from "react";
import BasicRunPage from "./internal/common/BasicRunPage";
import { CurrentPage } from "./internal/common/CurrentPage";
import styles from "./RunTestsPage.module.scss";
import TestResultComponent from "../../components/TestResultComponent/TestResultComponent";
import PlaceHolderText from "../../components/PlaceholderText/PlaceHolderText";
import { useHistory } from "react-router-dom";
import SuiteList from "./internal/SuiteList/SuiteList";
import FilterControls from "../../components/FilterControls/FilterControls";
import { updateQueryString } from "../../utils/queryStringUtils";
import { parseStateFromQueryString } from "./internal/common/extractRunTestAndSuitePageState";
interface Props {
  projectId: number;
  runId: number;
}

function RunSuitePage(props: Props) {
  const history = useHistory();
  const state = parseStateFromQueryString(history.location.search);
  return (
    <BasicRunPage {...props} currentPage={CurrentPage.SUITES}>
      <div className={styles.suiteAndTestContainer}>
        <div>
          <div className={styles.filterControlsContainer}>
            <FilterControls
              currentFilterOptions={state.currentFilterOptions}
              filterOptionsChanged={(filter) => {
                const queryString = updateQueryString(history.location.search, {
                  statusFilter: filter.status,
                });
                history.push({ search: queryString });
              }}
              failureReasonIsNotFilterable={true}
            />
          </div>
          <SuiteList
            projectId={props.projectId}
            runId={props.runId}
            filterOptions={state.currentFilterOptions}
          />
        </div>
        <div>
          <div>
            {state.selectedTest ? (
              <TestResultComponent
                runId={props.runId}
                projectId={props.projectId}
                resultId={state.selectedTest}
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
