import React, { Component } from "react";
import Project from "../../models/Project";
import styles from "./ProjectsView.module.css";
import LinkCard from "../linkcard/LinkCard";

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
            <div key={p.id} className={styles.projectsViewProjectComponent}>
              <LinkCard name={p.name} linkTo={`/projects/${p.id}/runs`} />
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
          this.setState({ projects: result });
        },
        (error) => {
          console.log(error);
        }
      );
  };
}

export default ProjectsView;
