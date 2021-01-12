import React, { Component } from "react";
import styles from "./RunSummary.module.scss";

import { Spinner } from "react-bootstrap";
import RunSummaryTabComponent from "./internal/RunSummaryTabComponent";
import { RunSummaryDto } from "../../catoapimodels";
import { formatDuration } from "../../utils";
import TestResultComponent from "../testresultcomponent/TestResultComponent";
import SuiteResultComponent from "../suiteresultcomponent/SuiteResultComponent";
import InfoBox from "../infobox/InfoBox";
import InfoBoxElement from "../infobox/InfoBoxElement";

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
        </div>
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
      <InfoBox>
        <InfoBoxElement
          value={"" + runSummaryDto.suite_count}
          title={"suites"}
        />
        <InfoBoxElement value={"" + runSummaryDto.test_count} title={"tests"} />
        <InfoBoxElement
          value={"" + runSummaryDto.failed_test_count}
          title={"failed tests"}
        />
        <InfoBoxElement
          value={
            "" +
            formatDuration(
              runSummaryDto.duration !== "NaN" ? runSummaryDto.duration : 0
            )
          }
          title={"duration"}
        />
      </InfoBox>
    );
  };

  renderSuiteOrTest = () => {
    return (
      <div className={styles.suiteOrTestContainer}>
        {this.props.currentTab === "suites" ? (
          <SuiteResultComponent
            suiteId={this.props.suiteOrTestId ? this.props.suiteOrTestId : 0}
            projectId={this.props.projectId}
            runId={this.props.runId}
          />
        ) : (
          <TestResultComponent
            resultId={this.props.suiteOrTestId ? this.props.suiteOrTestId : 0}
            projectId={this.props.projectId}
            runId={this.props.runId}
          />
        )}
      </div>
    );
  };
}

export default RunSummary;
