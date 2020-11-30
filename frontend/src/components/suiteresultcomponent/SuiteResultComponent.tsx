import React, { Component } from "react";
import SuiteResult from "../../models/SuiteResult";
import TestResult from "../../models/TestResult";
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
        <h2>{this.props.suiteResult.suite_name}</h2>
        {this.state.testResults.map((result: TestResult) => {
          return (
            <div>
              #{result.id}: {result.test_identifier.suite_name}/
              {result.test_identifier.test_name}
            </div>
          );
        })}
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
}

export default SuiteResultComponent;
