import React, { Component } from "react";
import styles from "./RunSummary.module.scss";
import { formatDuration } from "../../utils";
import { RunStatusDto, RunSummaryDto } from "../../catoapimodels";
import { Spinner } from "react-bootstrap";

interface Props {
  runId: number;
}

interface State {
  runSummaryDto: RunSummaryDto | null;
  isLoadingSummary: boolean;
}

class RunSummary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { runSummaryDto: null, isLoadingSummary: false };
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
      </div>
    );
  }

  renderInfoBox = (runSummaryDto: RunSummaryDto) => {
    return (
      <div className={styles.runSummaryInfoBox}>
        {this.renderInfoBoxElement("" + runSummaryDto.suiteCount, "suites")}
        {this.renderInfoBoxElement("" + runSummaryDto.testCount, "tests")}
        {this.renderInfoBoxElement(
          "" + runSummaryDto.failedTestCount,
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
}

export default RunSummary;
