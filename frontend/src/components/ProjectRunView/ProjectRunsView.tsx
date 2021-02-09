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
import SimplePaginationControls from "../Pagination/SimplePaginationControls";
import { Page, PageRequest, requestFirstPageOfSize } from "../Pagination/Page";

interface Props {
  projectId: number;
  currentRunId: number | null;
  currentTab: string | null;
  suiteOrTestId: number | null;
}

interface State {
  project: Project | null;
  runs?: Page<RunDto>;
  currentSuiteResults: SuiteResult[];
}

class ProjectRunsView extends Component<Props, State> {
  interval: any;

  constructor(props: Props) {
    super(props);
    this.state = { project: null, runs: undefined, currentSuiteResults: [] };

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
          <div>
            {this.state.runs ? (
              <React.Fragment>
                <SimplePaginationControls
                  currentPage={this.state.runs}
                  pageChangedCallback={(pageRequest) =>
                    this.fetchRuns(pageRequest)
                  }
                />
                <ListGroup className={styles.runListContainer}>
                  {this.state.runs.entities.map((r: RunDto) => {
                    return (
                      <RunListEntryComponent
                        key={r.id}
                        run={r}
                        isCurrentEntry={this.isCurrentEntry(r)}
                        link={`/projects/${this.props.projectId}/runs/${r.id}/${
                          this.props.currentTab
                            ? this.props.currentTab
                            : "suites"
                        }`}
                      />
                    );
                  })}
                </ListGroup>
              </React.Fragment>
            ) : (
              <React.Fragment />
            )}
          </div>
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
    this.fetchRuns(requestFirstPageOfSize(25));
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

  fetchRuns = (pageRequest: PageRequest) => {
    fetch(
      "/api/v1/runs/project/" +
        this.props.projectId +
        `?page_number=${pageRequest.page_number}&page_size=${pageRequest.page_size}`
    )
      .then((res) => res.json())
      .then(
        (result) => {
          result.entities.reverse();
          this.setState({ runs: result });
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
