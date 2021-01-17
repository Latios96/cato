import React, { Component } from "react";
import { Link } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import styles from "./ProjectRunsView.module.scss";
import { formatTime } from "../../utils";
import { RunDto } from "../../catoapimodels";
import RunStatus from "../Status/RunStatus";

interface Props {
  run: RunDto;
  isCurrentEntry: boolean;
  link: string;
}

interface State {}

class RunListEntryComponent extends Component<Props, State> {
  interval: any;

  constructor(props: Props) {
    super(props);
    this.state = { status: "" };
  }

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
            <RunStatus
              status={this.props.run.status}
              isActive={this.props.isCurrentEntry}
            />
          </ListGroup.Item>
        </Link>
      </div>
    );
  }
}

export default RunListEntryComponent;
