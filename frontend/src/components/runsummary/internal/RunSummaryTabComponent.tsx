import { Link, useHistory } from "react-router-dom";
import { ListGroup, Tab, Tabs } from "react-bootstrap";
import React, { useEffect, useState } from "react";
import SuiteResult from "../../../models/SuiteResult";
import styles from "./RunSummaryTabComponent.module.scss";
import TestResult from "../../../models/TestResult";

interface Props {
  projectId: number;
  runId: number;
  currentTab: string;
}

export default function RunSummaryTabComponent(props: Props) {
  const [currentTab, setCurrentTab] = useState(props.currentTab);
  const [suites, setSuites] = useState<SuiteResult[]>([]);
  const [tests, setTests] = useState<TestResult[]>([]);
  let history = useHistory();

  useEffect(() => {
    setCurrentTab(props.currentTab);
    if (currentTab === "tests") {
      console.log("fetching tests");
      fetch(`/api/v1/test_results/${props.runId}`)
        .then((res) => res.json())
        .then(
          (result) => {
            console.log(result);
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
            console.log(result);
            setSuites(result);
          },
          (error) => {
            console.log(error);
          }
        );
    }
  }, [currentTab, props.currentTab, props.runId]);

  console.log(currentTab, props.runId);

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
          <ListGroup>
            {suites.map((suite) => {
              return (
                <Link to={"test"}>
                  <ListGroup.Item className={styles.listEntry}>
                    {suite.suite_name}
                  </ListGroup.Item>
                </Link>
              );
            })}
          </ListGroup>
        </div>
      </Tab>
      <Tab eventKey="tests" title="Tests">
        <div className={styles.tabContent}>
          <ListGroup>
            {tests.map((test) => {
              return (
                <Link to={"test"}>
                  <ListGroup.Item className={styles.listEntry}>
                    {test.test_identifier}
                  </ListGroup.Item>
                </Link>
              );
            })}
          </ListGroup>
        </div>
      </Tab>
    </Tabs>
  );
}
