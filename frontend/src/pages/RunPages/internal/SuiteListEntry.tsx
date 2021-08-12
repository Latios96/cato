import React, { useEffect } from "react";
import { ChevronDown, ChevronRight } from "react-bootstrap-icons";
import SuiteStatus from "../../../components/Status/SuiteStatus";
import styles from "./SuiteListEntry.module.scss";
import { SuiteResultDto, TestResultDto } from "../../../catoapimodels";
import { useToggle } from "rooks";
import { CachePolicies, useFetch } from "use-http";
import {
  DataLoadedState,
  LoadingStateHandler,
} from "../../../components/LoadingStateHandler/LoadingStateHandler";
import { useHistory } from "react-router-dom";
import { popFromQueryString, updateQueryString } from "../../../utils";
import TestStatus from "../../../components/Status/TestStatus";
import queryString from "query-string";

interface Props {
  suite: SuiteResultDto;
  projectId: number;
  runId: number;
}

function SuiteListEntry(props: Props) {
  const history = useHistory();
  const [expanded, toggle] = useToggle(false);
  const { data, loading, get } = useFetch<TestResultDto[]>(
    `api/v1/test_results/suite_result/${props.suite.id}`,
    {
      cachePolicy: CachePolicies.NO_CACHE,
    }
  );
  useEffect(() => {
    if (expanded) {
      get();
    }
  }, [get, expanded]);

  const toggleExpansion = () => {
    let search = "";
    if (!expanded) {
      search = updateQueryString(history.location.search, {
        selectedSuite: props.suite.id,
      });
    } else {
      search = popFromQueryString(history.location.search, ["selectedSuite"]);
    }
    history.push({
      search,
    });
    toggle(true);
  };

  const queryParams = queryString.parse(history.location.search, {
    parseNumbers: true,
  });
  const selectedTest = queryParams.selectedTest;
  // todo error / loading state / no tests state
  return (
    <div>
      <div className={styles.suiteListEntry}>
        <span onClick={toggleExpansion}>
          {expanded ? <ChevronDown /> : <ChevronRight />}
        </span>
        <span>
          <SuiteStatus suiteResult={props.suite} />
        </span>
        <span>{props.suite.suite_name}</span>
      </div>
      <div>
        {expanded ? (
          <div className={styles.suiteListEntryContent}>
            <LoadingStateHandler isLoading={loading}>
              <DataLoadedState>
                {data ? (
                  <>
                    {data.length === 0 ? (
                      <div>
                        <span>This suite has no tests</span>
                      </div>
                    ) : null}
                    {data.map((test) => {
                      return (
                        <div
                          onClick={() =>
                            history.push({
                              search: updateQueryString(
                                history.location.search,
                                {
                                  selectedSuite: props.suite.id,
                                  selectedTest: test.id,
                                }
                              ),
                            })
                          }
                          className={
                            test.id === selectedTest ? styles.active : ""
                          }
                        >
                          <span>
                            <TestStatus testResult={test} />
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
        ) : (
          ""
        )}
      </div>
    </div>
  );
}

export default SuiteListEntry;
