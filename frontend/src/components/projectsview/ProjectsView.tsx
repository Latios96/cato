import React, { Component } from "react";
import Project from "../../models/Project";
import styles from "./ProjectsView.module.css";
import LinkCard from "../linkcard/LinkCard";
import PlaceHolderText from "../placeholdertext/PlaceHolderText";
import { Helmet } from "react-helmet";

interface Props {}

interface State {
  projects: Project[];
  isLoading: boolean;
}

class ProjectsView extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { projects: [], isLoading: true };
  }

  componentDidMount() {
    this.fetchProjects();
  }

  render() {
    return (
      <div className={styles.projectsView}>
        <Helmet>
          <title>Cato</title>
        </Helmet>
        {this.state.projects.length
          ? this.renderProjects()
          : this.renderPlaceholder()}
      </div>
    );
  }

  fetchProjects = () => {
    fetch("/api/v1/projects")
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ projects: result, isLoading: false });
        },
        (error) => {
          console.log(error);
        }
      );
  };

  renderProjects = () => {
    return this.state.projects.map((p: Project) => {
      return (
        <div key={p.id} className={styles.projectsViewProjectComponent}>
          <LinkCard name={p.name} linkTo={`/projects/${p.id}/runs`} />
        </div>
      );
    });
  };
  renderPlaceholder = () => {
    if (!this.state.isLoading) {
      return <PlaceHolderText text={"No projects found"} className={""} />;
    }
    return <React.Fragment />;
  };
}

export default ProjectsView;
