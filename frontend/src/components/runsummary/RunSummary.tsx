import React, { Component } from "react";
import styles from "./RunSummary.module.scss";
import { formatDuration } from "../../utils";
import { IRunDto, RunStatusDto } from "../../catoapimodels";

interface Props {
  runId: number;
}

interface IRunInfoDto {
  run: IRunDto;
  suiteCount: number;
  testCount: number;
  failedTestCount: number;
  duration: number;
}

interface State {
  runInfo: IRunInfoDto;
}

class RunSummary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      runInfo: {
        run: {
          id: 3,
          project_id: 3,
          started_at: "sdfsd",
          status: RunStatusDto.SUCCESS,
        },
        suiteCount: 2,
        testCount: 22,
        failedTestCount: 13,
        duration: 82,
      },
    };
  }

  render() {
    return (
      <div>
        <h3 className={styles.runSummaryHeadline}>
          Run Summary: #{this.props.runId}
        </h3>
        <div className={styles.runSummaryInfoBox}>
          {this.renderInfoBoxElement(
            "" + this.state.runInfo.suiteCount,
            "suites"
          )}
          {this.renderInfoBoxElement(
            "" + this.state.runInfo.testCount,
            "tests"
          )}
          {this.renderInfoBoxElement(
            "" + this.state.runInfo.failedTestCount,
            "failed tests"
          )}
          {this.renderInfoBoxElement(
            "" + formatDuration(this.state.runInfo.duration),
            "duration"
          )}
        </div>
      </div>
    );
  }

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
