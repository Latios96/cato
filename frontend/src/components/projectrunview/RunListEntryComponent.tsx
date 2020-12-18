import React, { Component } from "react";
import { Link } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import styles from "./ProjectRunsView.module.scss";
import { formatTime } from "../../utils";
import RenderingBucketIcon from "../icons/RenderingBucketIcon";
import { RunDto } from "../../catoapimodels";
import { Check2All, Hourglass } from "react-bootstrap-icons";
import { XCircleIcon } from "@primer/octicons-react";

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
            {this.renderRunStatus(
              this.props.run.status,
              this.props.isCurrentEntry
            )}
          </ListGroup.Item>
        </Link>
      </div>
    );
  }

  renderRunStatus = (status: string, isCurrentEntry: boolean) => {
    if (status === "NOT_STARTED") {
      return <Hourglass size={27} />;
    } else if (status === "RUNNING") {
      return <RenderingBucketIcon isActive={isCurrentEntry} />;
    } else if (status === "SUCCESS") {
      return <Check2All color="green" size={27} />;
    } else if (status === "FAILED") {
      return <XCircleIcon size={27} className={styles.errorIcon} />;
    }
    return <span />;
  };
}

export default RunListEntryComponent;
