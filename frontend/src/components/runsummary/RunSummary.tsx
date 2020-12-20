import React, { Component } from "react";
import styles from "./RunSummary.module.scss";

import { Spinner } from "react-bootstrap";
import RunSummaryTabComponent from "./internal/RunSummaryTabComponent";
import { RunSummaryDto } from "../../catoapimodels";
import { formatDuration } from "../../utils";
import TestResultComponent from "../testresultcomponent/TestResultComponent";
import SuiteResultComponent from "../suiteresultcomponent/SuiteResultComponent";

interface Props {
  projectId: number;
  runId: number;
  currentTab: string;
  suiteOrTestId: number | null;
}

interface State {
  runSummaryDto: RunSummaryDto | null;
  isLoadingSummary: boolean;
}

class RunSummary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      runSummaryDto: null,
      isLoadingSummary: false,
    };
  }

  componentDidMount() {
    this.fetchRunSummary();
  }
  componentDidUpdate(
    prevProps: Readonly<Props>,
    prevState: Readonly<State>,
    snapshot?: any
  ) {
    if (this.props.runId !== prevProps.runId) {
      this.fetchRunSummary();
    }
  }

  fetchRunSummary = () => {
    this.setState({ isLoadingSummary: true }, () => {
      fetch(`/api/v1/runs/${this.props.runId}/summary`)
        .then((res) => res.json())
        .then(
          (result) => {
            this.setState({ runSummaryDto: result, isLoadingSummary: false });
          },
          (error) => {
            console.log(error);
          }
        );
    });
  };

  render() {
    return (
      <div>
        <h3 className={styles.runSummaryHeadline}>
          Run Summary: #{this.props.runId}
        </h3>
        {this.state.isLoadingSummary ? (
          <div className={styles.runSummaryInfoBox}>
            <div className={styles.infoBoxLoading}>
              <Spinner animation="border" role="status">
                <span className="sr-only">Loading...</span>
              </Spinner>
            </div>
          </div>
        ) : this.state.runSummaryDto ? (
          this.renderInfoBox(this.state.runSummaryDto)
        ) : (
          <React.Fragment />
        )}
        {!this.props.suiteOrTestId ? (
          <div className={styles.runContent}>
            <RunSummaryTabComponent
              projectId={this.props.projectId}
              runId={this.props.runId}
              currentTab={this.props.currentTab}
            />
          </div>
        ) : (
          this.renderSuiteOrTest()
        )}
      </div>
    );
  }

  renderInfoBox = (runSummaryDto: RunSummaryDto) => {
    return (
      <div className={styles.runSummaryInfoBox}>
        {this.renderInfoBoxElement("" + runSummaryDto.suite_count, "suites")}
        {this.renderInfoBoxElement("" + runSummaryDto.test_count, "tests")}
        {this.renderInfoBoxElement(
          "" + runSummaryDto.failed_test_count,
          "failed tests"
        )}
        {this.renderInfoBoxElement(
          "" +
            formatDuration(
              runSummaryDto.duration !== "NaN" ? runSummaryDto.duration : 0
            ),
          "duration"
        )}
      </div>
    );
  };

  renderInfoBoxElement = (value: string, name: string) => {
    return (
      <div className={styles.infoBoxElement}>
        <span className={styles.runSummaryInfoBoxValue}>{value}</span>
        <span>{name}</span>
      </div>
    );
  };

  renderSuiteOrTest = () => {
    return (
      <div className={styles.suiteOrTestContainer}>
        {this.props.currentTab === "suites" ? (
          <SuiteResultComponent
            suiteId={this.props.suiteOrTestId ? this.props.suiteOrTestId : 0}
          />
        ) : (
          <TestResultComponent
            resultId={this.props.suiteOrTestId ? this.props.suiteOrTestId : 0}
          />
        )}
      </div>
    );
  };
}

export default RunSummary;
