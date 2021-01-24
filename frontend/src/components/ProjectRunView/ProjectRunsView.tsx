import React, { Component } from "react";
import { ListGroup } from "react-bootstrap";
import styles from "./ProjectRunsView.module.scss";
import SuiteResult from "../../models/SuiteResult";
import Project from "../../models/Project";
import RunListEntryComponent from "./RunListEntryComponent";
import RunSummary from "../RunSummary/RunSummary";
import { RunDto } from "../../catoapimodels";
import { Helmet } from "react-helmet";
import { renderIf } from "../utils";

interface Props {
  projectId: number;
  currentRunId: number | null;
  currentTab: string | null;
  suiteOrTestId: number | null;
}

interface State {
  project: Project | null;
  runs: RunDto[];
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
        <Helmet>
          <title>{this.state.project ? this.state.project.name : "Cato"}</title>
        </Helmet>

        {renderIf(this.state.project, (project) => {
          return <h1 className={styles.projectName}>{project.name}</h1>;
        })}

        <div className={styles.runsViewContainer}>
          <ListGroup className={styles.runListContainer}>
            {this.state.runs.map((r: RunDto) => {
              return (
                <RunListEntryComponent
                  key={r.id}
                  run={r}
                  isCurrentEntry={this.isCurrentEntry(r)}
                  link={`/projects/${this.props.projectId}/runs/${r.id}/${
                    this.props.currentTab ? this.props.currentTab : "suites"
                  }`}
                />
              );
            })}
          </ListGroup>
          <div className={styles.suiteResult}>
            {this.props.currentRunId
              ? this.renderRunSummary()
              : this.renderRunSummaryPlaceholder()}
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

  renderRunSummary = () => {
    return (
      <div>
        {this.props.currentRunId ? (
          <RunSummary
            projectId={this.props.projectId}
            runId={this.props.currentRunId}
            currentTab={
              this.props.currentTab ? this.props.currentTab : "suites"
            }
            suiteOrTestId={this.props.suiteOrTestId}
          />
        ) : (
          <React.Fragment />
        )}
      </div>
    );
  };

  renderRunSummaryPlaceholder = () => {
    return (
      <div>
        <span className={styles.suiteResultsPlaceholder}>
          Please select a run
        </span>
      </div>
    );
  };

  isCurrentEntry = (r: RunDto) => {
    return r.id === this.props.currentRunId;
  };
}

export default ProjectRunsView;