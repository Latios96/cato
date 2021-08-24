import React, { Component } from "react";
import styles from "./RunSummary.module.scss";

import { Spinner } from "react-bootstrap";
import { RunSummaryDto } from "../../catoapimodels";
import { formatDuration } from "../../utils/dateUtils";
import InfoBox from "../InfoBox/InfoBox";
import InfoBoxElement from "../InfoBox/InfoBoxElement/InfoBoxElement";

interface Props {
  projectId: number;
  runId: number;
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
          ) : this.state.runSummaryDto ? (
            this.renderInfoBox(this.state.runSummaryDto)
          ) : (
            <React.Fragment />
          )}
        </div>
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
              runSummaryDto.run.duration !== "NaN"
                ? runSummaryDto.run.duration
                : 0
            )
          }
          title={"duration"}
        />
      </InfoBox>
    );
  };
}

export default RunSummary;
