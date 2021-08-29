import React from "react";
import BasicRunPage from "./internal/common/BasicRunPage";
import { CurrentPage } from "./internal/common/CurrentPage";
import styles from "./RunTestsPage.module.scss";
import TestList from "./internal/TestList/TestList";
import { useHistory } from "react-router-dom";
import queryString from "query-string";
import TestResultComponent from "../../components/TestResultComponent/TestResultComponent";
import PlaceHolderText from "../../components/PlaceholderText/PlaceHolderText";
import FilterControls from "../../components/FilterControls/FilterControls";
import { updateQueryString } from "../../utils/queryStringUtils";
import { testResultFilterOptionsFromQueryString } from "../../utils/filterOptionUtils";
import { FilterOptions } from "../../models/FilterOptions";

interface Props {
  projectId: number;
  runId: number;
}

function RunTestsPage(props: Props) {
  const history = useHistory();
  const state = parseStateFromQueryString(history.location.search);
  return (
    <BasicRunPage {...props} currentPage={CurrentPage.TESTS}>
      <div className={styles.suiteAndTestContainer}>
        <div>
          <div className={styles.filterControlsContainer}>
            <FilterControls
              currentFilterOptions={state.currentFilterOptions}
              statusFilterChanged={(filter) => {
                const queryString = updateQueryString(history.location.search, {
                  statusFilter: filter,
                });
                history.push({ search: queryString });
              }}
            />
          </div>
          <TestList
            projectId={props.projectId}
            runId={props.runId}
            testResultFilterOptions={state.currentFilterOptions}
            selectedTestId={state.selectedTest}
            selectedTestIdChanged={(testId) => {
              history.push({
                search: updateQueryString(history.location.search, {
                  selectedTest: testId,
                }),
              });
            }}
          />
        </div>
        <div id={"selectedTestContainer"}>
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
interface State {
  currentFilterOptions: FilterOptions;
  selectedTest: number | undefined;
}
function parseStateFromQueryString(theQueryString: string): State {
  const queryParams = queryString.parse(theQueryString, {
    parseNumbers: true,
  });

  const currentFilterOptions =
    testResultFilterOptionsFromQueryString(theQueryString);
  const state = {
    currentFilterOptions,
    selectedTest: undefined,
  };
  if (
    queryParams.selectedTest &&
    !Array.isArray(queryParams.selectedTest) &&
    !(typeof queryParams.selectedTest === "string")
  ) {
    return {
      ...state,
      selectedTest: queryParams.selectedTest,
    };
  }
  return state;
}

export default RunTestsPage;
