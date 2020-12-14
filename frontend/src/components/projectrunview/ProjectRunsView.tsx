import React, { Component } from "react";
import Run from "../../models/Run";
import { ListGroup } from "react-bootstrap";
import styles from "./ProjectRunsView.module.css";
import SuiteResult from "../../models/SuiteResult";
import Project from "../../models/Project";
import RunListEntryComponent from "./RunListEntryComponent";
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
  interval: any;

  constructor(props: Props) {
    super(props);
    this.state = { project: null, runs: [], currentSuiteResults: [] };
    this.interval = 0;
  }

  componentDidMount() {
    this.update();
    this.interval = setInterval(() => this.fetchRuns(), 10000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
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
        <h1 className={styles.projectName}>{this.state.project?.name}</h1>
        <div className={styles.runsViewContainer}>
          <ListGroup>
            {this.state.runs.map((r: Run) => {
              return (
                <RunListEntryComponent
                  key={r.id}
                  run={r}
                  isCurrentEntry={this.isCurrentEntry(r)}
                  link={`/projects/${this.props.projectId}/runs/${r.id}`}
                />
              );
            })}
          </ListGroup>
          <div className={styles.suiteResult}>
            {this.state.currentSuiteResults.length !== 0
              ? this.renderSuiteResults(this.state.currentSuiteResults)
              : this.renderSuiteResultsPlaceholder()}
          </div>
        </div>
      </div>
    );
  }

  update = () => {
    this.fetchProject();
    this.fetchRuns();
    this.fetchSuiteResults();
  };

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
          this.setState({ runs: result.reverse() });
        },
        (error) => {
          console.log(error);
        }
      );
  };

  fetchSuiteResults = () => {
    fetch(
      "/api/v1/suite_results/run/" +
        (this.props.currentRunId ? this.props.currentRunId : "0")
    )
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ currentSuiteResults: result });
        },
        (error) => {
          console.log(error);
        }
      );
  };

  renderSuiteResults = (suiteResults: SuiteResult[]) => {
    return suiteResults.map((suiteResult: SuiteResult) => {
      return (
        <div>
          <SuiteResultComponent suiteResult={suiteResult} />
        </div>
      );
    });
  };

  renderSuiteResultsPlaceholder = () => {
    return (
      <div>
        <span className={styles.suiteResultsPlaceholder}>
          Please select a run
        </span>
      </div>
    );
  };

  isCurrentEntry = (r: Run) => {
    return r.id === this.props.currentRunId;
  };
}

export default ProjectRunsView;
