import { useHistory } from "react-router-dom";
import { Spinner, Tab, Tabs } from "react-bootstrap";
import React, { useEffect, useState } from "react";
import styles from "./RunSummaryTabComponent.module.scss";
import { SuiteResultDto, TestResultDto } from "../../../catoapimodels";
import SuiteResultList from "../../SuiteAndTestsLists/SuiteResultList";
import TestResultList from "../../SuiteAndTestsLists/TestResultList";

interface Props {
  projectId: number;
  runId: number;
  currentTab: string;
}

export default function RunSummaryTabComponent(props: Props) {
  const [currentTab, setCurrentTab] = useState(props.currentTab);
  const [suites, setSuites] = useState<SuiteResultDto[]>([]);
  const [tests, setTests] = useState<TestResultDto[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  let history = useHistory();

  useEffect(() => {
    setCurrentTab(props.currentTab);
    setIsLoading(true);
    if (currentTab === "tests") {
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
    } else {
      fetch(`/api/v1/suite_results/run/${props.runId}`)
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
          {isLoading ? (
            renderSpinner()
          ) : (
            <SuiteResultList
              suiteResults={suites}
              projectId={props.projectId}
              runId={props.runId}
            />
          )}
        </div>
      </Tab>
      <Tab eventKey="tests" title="Tests">
        <div className={styles.tabContent}>
          {isLoading ? (
            renderSpinner()
          ) : (
            <TestResultList
              testResults={tests}
              projectId={props.projectId}
              runId={props.runId}
            />
          )}
        </div>
      </Tab>
    </Tabs>
  );
}
