import { useHistory } from "react-router-dom";
import { Spinner, Tab, Tabs } from "react-bootstrap";
import React, { useEffect, useState } from "react";
import styles from "./RunSummaryTabComponent.module.scss";
import { SuiteResultDto, TestResultDto } from "../../../catoapimodels";
import SuiteResultList from "../../SuiteAndTestsLists/SuiteResultList";
import TestResultList from "../../SuiteAndTestsLists/TestResultList";
import SimplePaginationControls from "../../Pagination/SimplePaginationControls";
import {
  Page,
  PageRequest,
  requestFirstPageOfSize,
} from "../../Pagination/Page";

interface Props {
  projectId: number;
  runId: number;
  currentTab: string;
}

export default function RunSummaryTabComponent(props: Props) {
  const [currentTab, setCurrentTab] = useState(props.currentTab);
  const [suites, setSuites] = useState<Page<SuiteResultDto>>();
  const [tests, setTests] = useState<Page<TestResultDto>>();
  const [isLoading, setIsLoading] = useState(true);
  let history = useHistory();

  useEffect(() => {
    setCurrentTab(props.currentTab);
    setIsLoading(true);

    const fetchTests = (pageRequest: PageRequest) => {
      fetch(
        `/api/v1/test_results/run/${props.runId}?page_number=${pageRequest.page_number}&page_size=${pageRequest.page_size}`
      )
        .then((res) => res.json())
        .then(
          (result) => {
            setTests(result);
            setIsLoading(false);
          },
          (error) => {
            console.log(error);
            setIsLoading(false);
          }
        );
    };

    const fetchSuites = (pageRequest: PageRequest) => {
      fetch(
        `/api/v1/suite_results/run/${props.runId}?page_number=${pageRequest.page_number}&page_size=${pageRequest.page_size}`
      )
        .then((res) => res.json())
        .then(
          (result) => {
            setSuites(result);
            setIsLoading(false);
          },
          (error) => {
            console.log(error);
            setIsLoading(false);
          }
        );
    };
    const firstPage = requestFirstPageOfSize(25);
    if (currentTab === "tests") {
      fetchTests(firstPage);
    } else {
      fetchSuites(firstPage);
    }
  }, [currentTab, props.currentTab, props.runId]);

  let renderSpinner = () => {
    return (
      <div className={styles.spinnerContainer}>
        <Spinner animation="border" role="status" className={styles.spinner}>
          <span className="sr-only">Loading...</span>
        </Spinner>
      </div>
    );
  };

  return (
    <Tabs
      id="controlled-tab-example"
      activeKey={currentTab}
      onSelect={(k) =>
        history.push(`/projects/${props.projectId}/runs/${props.runId}/${k}`)
      }
      transition={false}
    >
      <Tab eventKey="suites" title="Suites">
        <div className={styles.tabContent}>
          {isLoading || suites === undefined ? (
            renderSpinner()
          ) : (
            <>
              <SimplePaginationControls
                currentPage={suites}
                pageChangedCallback={(pageRequest) => {
                  fetch(`/api/v1/test_results/run/${props.runId}`)
                    .then((res) => res.json())
                    .then(
                      (result) => {
                        setTests(result);
                        setIsLoading(false);
                      },
                      (error) => {
                        console.log(error);
                        setIsLoading(false);
                      }
                    );
                }}
              />
              <SuiteResultList
                suiteResults={suites.entities}
                projectId={props.projectId}
                runId={props.runId}
                isLoading={isLoading}
              />
            </>
          )}
        </div>
      </Tab>
      <Tab eventKey="tests" title="Tests">
        <div className={styles.tabContent}>
          {isLoading || tests === undefined ? (
            renderSpinner()
          ) : (
            <>
              <SimplePaginationControls
                currentPage={tests}
                pageChangedCallback={(pageRequest) => {
                  fetch(
                    `/api/v1/test_results/run/${props.runId}?page_number=${pageRequest.page_number}&page_size=${pageRequest.page_size}`
                  )
                    .then((res) => res.json())
                    .then(
                      (result) => {
                        setTests(result);
                        setIsLoading(false);
                      },
                      (error) => {
                        console.log(error);
                        setIsLoading(false);
                      }
                    );
                }}
              />
              <TestResultList
                testResults={tests.entities}
                projectId={props.projectId}
                runId={props.runId}
                isLoading={isLoading}
              />
            </>
          )}
        </div>
      </Tab>
    </Tabs>
  );
}
