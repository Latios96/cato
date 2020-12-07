import React, { Component } from "react";
import Run from "../../models/Run";
import { Link } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import styles from "./ProjectRunsView.module.css";
import { formatTime } from "../../utils";
interface Props {
  run: Run;
  isCurrentEntry: boolean;
  link: string;
}
interface State {}
class RunListEntryComponent extends Component<Props, State> {
  render() {
    return (
      <div>
        <Link to={this.props.link}>
          <ListGroup.Item
            className={styles.runListEntry}
            active={this.props.isCurrentEntry}
          >
            <span className={styles.runNumber}>Run #{this.props.run.id}</span>{" "}
            <span className={styles.runTimingInformation}>
              {formatTime(this.props.run.started_at)}
            </span>
          </ListGroup.Item>
        </Link>
      </div>
    );
  }
}

export default RunListEntryComponent;
