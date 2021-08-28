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
import { StatusFilter } from "../../catoapimodels";
import { updateQueryString } from "../../utils/queryStringUtils";

interface Props {
  projectId: number;
  runId: number;
}

function RunTestsPage(props: Props) {
  const history = useHistory();
  const queryParams = queryString.parse(history.location.search, {
    parseNumbers: true,
  });
  // @ts-ignore
  const selectedTestId: number = queryParams.selectedTest;
  // @ts-ignore
  const currentFilter: StatusFilter | undefined = queryParams.filter;
  return (
    <BasicRunPage {...props} currentPage={CurrentPage.TESTS}>
      <div className={styles.suiteAndTestContainer}>
        <div>
          <div className={styles.filterControlsContainer}>
            <FilterControls
              currentFilter={currentFilter ? currentFilter : StatusFilter.NONE}
              filterChanged={(filter) => {
                const queryString = updateQueryString(history.location.search, {
                  filter: filter,
                });
                history.push({ search: queryString });
              }}
            />
          </div>
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
