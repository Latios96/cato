import React, { Component } from "react";
import Run from "../../models/Run";
import ago from "s-ago";
import { ListGroup } from "react-bootstrap";
import styles from "./ProjectRunsView.module.css";
import { Link } from "react-router-dom";
import SuiteResult from "../../models/SuiteResult";
import Project from "../../models/Project";
import SuiteResultComponent from "../suiteresultcomponent/SuiteResultComponent";

interface Props {
  projectId: number;
  currentRunId: number | null;
}
interface State {
  project: Project | null;
  runs: Run[];
  currentSuiteResults: SuiteResult[];
}
class ProjectRunsView extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { project: null, runs: [], currentSuiteResults: [] };
  }
  componentDidMount() {
    this.fetchProject();
    this.fetchRuns();
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
        <h1>{this.state.project?.name}</h1>
        <div className={styles.runsViewContainer}>
          <ListGroup>
            {this.state.runs.reverse().map((r: Run) => {
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
          <div>
            {this.state.currentSuiteResults.map((suiteResult: SuiteResult) => {
              return (
                <div>
                  <SuiteResultComponent suiteResult={suiteResult} />
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }
  fetchProject = () => {
    fetch("/api/v1/projects/" + this.props.projectId)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ project: result });
        },
        (error) => {
          console.log(error);
        }
      );
  };

  fetchRuns = () => {
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
    if (!this.props.currentRunId) {
      return;
    }
    fetch("/api/v1/suite_results/run/" + this.props.currentRunId)
      .then((res) => res.json())
      .then(
        (result) => {
          console.log(result);
          this.setState({ currentSuiteResults: result });
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
