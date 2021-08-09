import React from "react";
import { TestResultShortSummaryDto } from "../../../catoapimodels";
import styles from "./TestList.module.scss";
import { useHistory, useLocation } from "react-router-dom";
import queryString from "query-string";
import TestStatus from "../../../components/Status/TestStatus";
interface Props {
  projectId: number;
  runId: number;
  tests: TestResultShortSummaryDto[];
}

function TestList(props: Props) {
  const history = useHistory();
  const location = useLocation();
  const queryParams = queryString.parse(location.search, {
    parseNumbers: true,
  });
  const selectedTestId = queryParams.selectedTest;
  return (
    <table className={styles.testList}>
      <colgroup>
        <col />
        <col />
        <col />
      </colgroup>
      <tbody>
        {props.tests.map((test) => {
          return (
            <tr
              onClick={() =>
                history.push(
                  `/projects/${props.projectId}/runs/${props.runId}/tests/?selectedTest=${test.id}`
                )
              }
              className={test.id === selectedTestId ? styles.active : ""}
            >
              <td>
                <TestStatus testResult={test} />
              </td>
              <td>{test.test_identifier.split("/")[0]}</td>
              <td>{test.test_identifier.split("/")[1]}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default TestList;
