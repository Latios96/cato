import { useHistory } from "react-router-dom";
import { Tab, Tabs } from "react-bootstrap";
import React, { useEffect, useState } from "react";
import styles from "./RunSummaryTabComponent.module.scss";
import { SuiteResultDto, TestResultDto } from "../../../catoapimodels";
import SuiteResultList from "../../suiteandtestslists/SuiteResultList";
import TestResultList from "../../suiteandtestslists/TestResultList";

interface Props {
  projectId: number;
  runId: number;
  currentTab: string;
}

export default function RunSummaryTabComponent(props: Props) {
  const [currentTab, setCurrentTab] = useState(props.currentTab);
  const [suites, setSuites] = useState<SuiteResultDto[]>([]);
  const [tests, setTests] = useState<TestResultDto[]>([]);
  let history = useHistory();

  useEffect(() => {
    setCurrentTab(props.currentTab);
    if (currentTab === "tests") {
      fetch(`/api/v1/test_results/run/${props.runId}`)
        .then((res) => res.json())
        .then(
          (result) => {
            setTests(result);
          },
          (error) => {
            console.log(error);
          }
        );
    } else {
      console.log("fetching suites");
      fetch(`/api/v1/suite_results/run/${props.runId}`)
        .then((res) => res.json())
        .then(
          (result) => {
            setSuites(result);
          },
          (error) => {
            console.log(error);
          }
        );
    }
  }, [currentTab, props.currentTab, props.runId]);

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
          <SuiteResultList
            suiteResults={suites}
            projectId={props.projectId}
            runId={props.runId}
          />
        </div>
      </Tab>
      <Tab eventKey="tests" title="Tests">
        <div className={styles.tabContent}>
          <TestResultList
            testResults={tests}
            projectId={props.projectId}
            runId={props.runId}
          />
        </div>
      </Tab>
    </Tabs>
  );
}
