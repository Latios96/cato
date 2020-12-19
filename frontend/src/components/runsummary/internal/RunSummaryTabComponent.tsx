import { Link, useHistory } from "react-router-dom";
import { ListGroup, Tab, Tabs } from "react-bootstrap";
import React, { useEffect, useState } from "react";
import SuiteResult from "../../../models/SuiteResult";
import styles from "./RunSummaryTabComponent.module.scss";

interface Props {
  projectId: number;
  runId: number;
  currentTab: string;
}

export default function RunSummaryTabComponent(props: Props) {
  const [currentTab, setCurrentTab] = useState(props.currentTab);
  const [suites, setSuites] = useState<SuiteResult[]>([]);
  let history = useHistory();

  useEffect(() => {
    setCurrentTab(props.currentTab);
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
  }, [props.currentTab, props.runId]);

  return (
    <Tabs
      id="controlled-tab-example"
      activeKey={currentTab}
      onSelect={(k) =>
        history.push(`/projects/${props.projectId}/runs/${props.runId}/${k}`)
      }
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
    </Tabs>
  );
}
