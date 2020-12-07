import React, { Component } from "react";
import Run from "../../models/Run";
import { Link } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import styles from "./ProjectRunsView.module.css";
import { formatTime } from "../../utils";
import { GridLoader } from "react-spinners";
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
            {this.renderRunStatus(this.state.status)}
          </ListGroup.Item>
        </Link>
      </div>
    );
  }
  renderRunStatus = (status: string) => {
    if (status === "NOT_STARTED") {
      return <span>☐</span>;
    } else if (status === "RUNNING") {
      return <GridLoader size={5} />;
    } else if (status === "SUCCESS") {
      return "✔";
    } else if (status === "FAILED") {
      return "❌";
    }
    return <span />;
  };
}

export default RunListEntryComponent;
