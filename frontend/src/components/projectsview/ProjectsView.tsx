import React, { Component } from "react";
import ProjectComponent from "../project/ProjectComponent";
import Project from "../../models/Project";
import styles from "./ProjectsView.module.css";

interface Props {}

interface State {
  projects: Project[];
}

class ProjectsView extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { projects: [] };
  }

  componentDidMount() {
    this.fetchProjects();
  }

  render() {
    return (
      <div className={styles.projectsView}>
        {this.state.projects.map((p: Project) => {
          return (
            <div className={styles.projectsViewProjectComponent}>
              <ProjectComponent project={p} />
            </div>
          );
        })}
      </div>
    );
  }

  fetchProjects = () => {
    fetch("/api/v1/projects")
      .then((res) => res.json())
      .then(
        (result) => {
          console.log(result);
          this.setState({ projects: result });
        },
        (error) => {
          console.log(error);
        }
      );
  };
}

export default ProjectsView;
