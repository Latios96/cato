import React, { Component } from "react";
import Run from "../../models/Run";
import { Link } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import styles from "./ProjectRunsView.module.scss";
import { formatTime } from "../../utils";
import RenderingBucketIcon from "../icons/RenderingBucketIcon";
interface Props {
  run: Run;
  isCurrentEntry: boolean;
  link: string;
}
interface State {
  status: string;
}
class RunListEntryComponent extends Component<Props, State> {
  interval: any;
  constructor(props: Props) {
    super(props);
    this.state = { status: "" };
  }
  componentDidUpdate(
    prevProps: Readonly<Props>,
    prevState: Readonly<State>,
    snapshot?: any
  ) {
    if (prevProps.run.id !== this.props.run.id) {
      this.fetchStatus();
    }
  }

  componentDidMount() {
    this.fetchStatus();
    this.interval = setInterval(() => this.fetchStatus(), 10000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  fetchStatusInBg = () => {
    if (this.state.status === "SUCCESS" || this.state.status === "FAILED") {
      return;
    }
    this.fetchStatus();
  };

  fetchStatus = () => {
    fetch(`/api/v1/runs/${this.props.run.id}/status`)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ status: result.status });
        },
        (error) => {
          console.log(error);
        }
      );
  };

  render() {
    return (
      <div>
        <Link to={this.props.link}>
          <ListGroup.Item
            className={styles.runListEntry}
            active={this.props.isCurrentEntry}
          >
            <div className={styles.runNumber}>Run #{this.props.run.id}</div>{" "}
            <div className={styles.runTimingInformation}>
              {formatTime(this.props.run.started_at)}
            </div>
            {this.renderRunStatus(this.state.status, this.props.isCurrentEntry)}
          </ListGroup.Item>
        </Link>
      </div>
    );
  }
  renderRunStatus = (status: string, isCurrentEntry: boolean) => {
    if (status === "NOT_STARTED") {
      return <span>☐</span>;
    } else if (status === "RUNNING") {
      return <RenderingBucketIcon isActive={isCurrentEntry} />;
    } else if (status === "SUCCESS") {
      return "✔";
    } else if (status === "FAILED") {
      return "❌";
    }
    return <span />;
  };
}

export default RunListEntryComponent;
