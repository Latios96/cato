import React from "react";
import { Link } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import styles from "./SuiteAndTestLists.module.scss";
import TestStatus from "../Status/TestStatus";
import { ExecutionStatusDto, TestStatusDto } from "../../catoapimodels";
import PlaceHolderText from "../PlaceholderText/PlaceHolderText";

interface TestResultListListEntry {
  id: number;
  test_identifier: string;
  execution_status: ExecutionStatusDto;
  status: TestStatusDto;
}

interface Props {
  testResults: TestResultListListEntry[];
  projectId: number;
  runId: number;
  isLoading: boolean;
  displayOnlyTestName?: boolean;
}
const TestResultList = (props: Props) => {
  let renderPlaceholder = () => {
    return (
      <div className={styles.placeholderContainer}>
        <PlaceHolderText
          text={"No tests found"}
          className={styles.placeholder}
        />
      </div>
    );
  };

  let renderList = () => {
    return (
      <ListGroup>
        {props.testResults.map((test) => {
          return (
            <Link
              to={`/projects/${props.projectId}/runs/${props.runId}/tests/${test.id}`}
            >
              <ListGroup.Item className={styles.listEntry}>
                <span className={styles.statusInList}>
                  <TestStatus testResult={test} />
                </span>
                <span className={styles.nameInList}>
                  {!!props.displayOnlyTestName
                    ? test.test_identifier.split("/")[1]
                    : test.test_identifier}
                </span>
              </ListGroup.Item>
            </Link>
          );
        })}
      </ListGroup>
    );
  };

  if (!props.testResults.length && !props.isLoading) {
    return renderPlaceholder();
  }
  return renderList();
};

export default TestResultList;
