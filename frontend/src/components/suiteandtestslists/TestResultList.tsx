import React from "react";
import { Link } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import styles from "./SuiteAndTestLists.module.scss";
import TestStatus from "../status/TestStatus";
import { ExecutionStatusDto, TestStatusDto } from "../../catoapimodels";

interface TestResultListListEntry {
  id: number;
  testIdentifier: string;
  executionStatus: ExecutionStatusDto;
  status: TestStatusDto;
}

interface Props {
  testResults: TestResultListListEntry[];
}
const TestResultList = (props: Props) => {
  return (
    <ListGroup>
      {props.testResults.map((test) => {
        return (
          <Link to={`tests/${test.id}`}>
            <ListGroup.Item className={styles.listEntry}>
              <span className={styles.statusInList}>
                <TestStatus restResult={test} />
              </span>
              <span className={styles.nameInList}>{test.testIdentifier}</span>
            </ListGroup.Item>
          </Link>
        );
      })}
    </ListGroup>
  );
};

export default TestResultList;
