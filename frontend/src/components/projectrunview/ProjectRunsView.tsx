import React, { Component } from "react";
import Run from "../../models/Run";
import ago from "s-ago";
import { ListGroup } from "react-bootstrap";
import styles from "./ProjectRunsView.module.css";
import { Link } from "react-router-dom";
import SuiteResult from "../../models/SuiteResult";

interface Props {
  projectId: number;
  currentRunId: number | null;
}
interface State {
  runs: Run[];
  currentSuite: SuiteResult | null;
}
class ProjectRunsView extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { runs: [], currentSuite: null };
  }
  componentDidMount() {
    this.fetchProjects();
    this.fetchSuiteResults();
  }

  componentDidUpdate(
    prevProps: Readonly<Props>,
    prevState: Readonly<State>,
    snapshot?: any
  ) {
    if (prevProps.currentRunId !== this.props.currentRunId) {
      this.fetchSuiteResults();
    }
  }

  render() {
    return (
      <div>
        <ListGroup>
          {this.state.runs.map((r: Run) => {
            return (
              <div>
                <Link to={`/projects/${this.props.projectId}/runs/${r.id}`}>
                  <ListGroup.Item
                    className={styles.runListEntry}
                    active={this.isCurrentEntry(r)}
                  >
                    <p>Run #{r.id}</p>
                    <p>{this.formatTime(r.started_at)}</p>
                  </ListGroup.Item>
                </Link>
              </div>
            );
          })}
        </ListGroup>
      </div>
    );
  }
  fetchProjects = () => {
    fetch("/api/v1/runs/project/" + this.props.projectId)
      .then((res) => res.json())
      .then(
        (result) => {
          console.log(result);
          this.setState({ runs: result });
        },
        (error) => {
          console.log(error);
        }
      );
  };

  fetchSuiteResults = () => {
    fetch("/api/v1/suite_results/run/" + this.props.currentRunId)
      .then((res) => res.json())
      .then(
        (result) => {
          console.log(result);
          this.setState({ currentSuite: result });
        },
        (error) => {
          console.log(error);
        }
      );
  };

  formatTime = (datestr: string) => {
    var date = new Date(datestr);
    return ago(date);
  };
  isCurrentEntry = (r: Run) => {
    return r.id === this.props.currentRunId;
  };
}

export default ProjectRunsView;
