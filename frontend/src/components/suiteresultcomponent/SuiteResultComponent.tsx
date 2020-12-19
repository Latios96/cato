import React, { Component } from "react";
import { Card } from "react-bootstrap";
import SuiteResult from "../../models/SuiteResult";
import TestResult from "../../models/TestResult";
import styles from "./SuiteResultComponent.module.css";
import FinishedTestResultComponent from "../testresultcomponent/FinishedTestResultComponent";
import WaitingOrRunningTestResultComponent from "../testresultcomponent/WaitingOrRunningTestResultComponent";
interface Props {
  suiteResult: SuiteResult;
}
interface State {
  testResults: TestResult[];
}
class SuiteResultComponent extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { testResults: [] };
  }

  componentDidMount() {
    this.fetchTestResults();
  }

  componentDidUpdate(
    prevProps: Readonly<Props>,
    prevState: Readonly<State>,
    snapshot?: any
  ) {
    if (this.props.suiteResult.id !== prevProps.suiteResult.id) {
      this.fetchTestResults();
    }
  }

  render() {
    return (
      <div>
        {this.filterResults(this.state.testResults, "RUNNING").map(
          (result: TestResult) => {
            return this.renderResult(result);
          }
        )}
        {this.filterResults(this.state.testResults, "NOT_STARTED").map(
          (result: TestResult) => {
            return this.renderResult(result);
          }
        )}
        {this.filterResults(this.state.testResults, "FINISHED").map(
          (result: TestResult) => {
            return this.renderResult(result);
          }
        )}
      </div>
    );
  }

  fetchTestResults = () => {
    fetch("/api/v1/test_results/suite_result/" + this.props.suiteResult.id)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ testResults: result });
        },
        (error) => {
          console.log(error);
        }
      );
  };
  filterResults = (results: TestResult[], status: string) => {
    return results.filter((r: TestResult) => r.execution_status === status);
  };

  renderResult = (result: TestResult) => {
    return (
      <div key={result.id} className={styles.suiteResultCard}>
        <Card>
          <Card.Body>
            <Card.Title>
              {result.test_identifier.split("/")[0]} /{" "}
              {result.test_identifier.split("/")[1]}{" "}
              {this.emojinizeStatus(result.status)}
            </Card.Title>
            {result.execution_status === "FINISHED" ? (
              <FinishedTestResultComponent result={result} />
            ) : (
              <WaitingOrRunningTestResultComponent result={result} />
            )}
          </Card.Body>
        </Card>
      </div>
    );
  };
  emojinizeStatus = (status: string | null) => {
    if (status === "SUCCESS") {
      return "✔";
    } else if (status === "FAILED") {
      return "❌";
    }
    return "";
  };
}

export default SuiteResultComponent;
