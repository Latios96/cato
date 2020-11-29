import React, { Component } from "react";
import Run from "../../models/Run";
import ago from "s-ago";
import { ListGroup } from "react-bootstrap";
interface Props {
  projectId: number;
}
interface State {
  runs: Run[];
}
class ProjectRunsView extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { runs: [] };
  }
  componentDidMount() {
    this.fetchProjects();
  }

  render() {
    return (
      <div>
        <ListGroup>
          {this.state.runs.map((r: Run) => {
            return (
              <div>
                <ListGroup.Item>
                  <p>Run {r.id}</p>
                  <p>{this.formatTime(r.started_at)}</p>
                </ListGroup.Item>
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
  formatTime = (datestr: string) => {
    var date = new Date(datestr);
    return ago(date);
  };
}

export default ProjectRunsView;
