import React, { Component } from "react";
import styles from "./RunSummary.module.scss";

import { Spinner } from "react-bootstrap";
import { formatDuration } from "../../utils/dateUtils";
import InfoBox from "../InfoBox/InfoBox";
import InfoBoxElement from "../InfoBox/InfoBoxElement/InfoBoxElement";
import { RunAggregate } from "../../catoapimodels/catoapimodels";

interface Props {
  projectId: number;
  runId: number;
}

interface State {
  runAggregate: RunAggregate | null;
  isLoadingSummary: boolean;
}

class RunSummary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      runAggregate: null,
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
      fetch(`/api/v1/runs/${this.props.runId}/aggregate`)
        .then((res) => res.json())
        .then(
          (result) => {
            this.setState({ runAggregate: result, isLoadingSummary: false });
          },
          (error) => {}
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
          ) : this.state.runAggregate ? (
            this.renderInfoBox(this.state.runAggregate)
          ) : (
            <React.Fragment />
          )}
        </div>
      </div>
    );
  }

  renderInfoBox = (runAggregate: RunAggregate) => {
    return (
      <InfoBox>
        <InfoBoxElement value={"" + runAggregate.suiteCount} title={"suites"} />
        <InfoBoxElement value={"" + runAggregate.testCount} title={"tests"} />
        <InfoBoxElement
          value={"" + runAggregate.progress.failedTestCount}
          title={"failed tests"}
        />
        <InfoBoxElement
          value={"" + formatDuration(runAggregate.duration)}
          title={"duration"}
        />
      </InfoBox>
    );
  };
}

export default RunSummary;
