import { Link, useHistory } from "react-router-dom";
import { ListGroup, Tab, Tabs } from "react-bootstrap";
import React, { useEffect, useState } from "react";
import SuiteResult from "../../../models/SuiteResult";
import styles from "./RunSummaryTabComponent.module.scss";
import TestResult from "../../../models/TestResult";
import { Check, Hourglass } from "react-bootstrap-icons";
import RenderingBucketIcon from "../../icons/RenderingBucketIcon";
import { XCircleIcon } from "@primer/octicons-react";

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

  let testStatus = (test: TestResult) => {
    if (test.execution_status === "NOT_STARTED") {
      return <Hourglass size={27} />;
    } else if (test.execution_status === "RUNNING") {
      return <RenderingBucketIcon isActive={false} />;
    } else if (test.status === "SUCCESS") {
      return <Check color="green" size={27} />;
    } else if (test.status === "FAILED") {
      return <XCircleIcon size={27} className={styles.errorIcon} />;
    }
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
          <ListGroup>
            {suites.map((suite) => {
              return (
                <Link to={`suites/${suite.id}`}>
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
                <Link to={`tests/${test.id}`}>
                  <ListGroup.Item className={styles.listEntry}>
                    <span className={styles.statusInList}>
                      {testStatus(test)}
                    </span>
                    <span className={styles.nameInList}>
                      {test.test_identifier}
                    </span>
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
