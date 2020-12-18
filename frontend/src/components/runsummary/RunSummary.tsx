import React, { Component } from "react";
import styles from "./RunSummary.module.scss";
import { formatDuration } from "../../utils";
import { RunStatusDto, RunSummaryDto } from "../../catoapimodels";

interface Props {
  runId: number;
}

interface State {
  runSummaryDto: RunSummaryDto | null;
}

class RunSummary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { runSummaryDto: null };
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
    fetch(`/api/v1/runs/${this.props.runId}/summary`)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ runSummaryDto: result });
        },
        (error) => {
          console.log(error);
        }
      );
  };

  render() {
    return (
      <div>
        <h3 className={styles.runSummaryHeadline}>
          Run Summary: #{this.props.runId}
        </h3>
        {this.state.runSummaryDto ? (
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
