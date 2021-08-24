import React from "react";
import Project from "../../models/Project";
import styles from "./ProjectsView.module.css";
import LinkCard from "../LinkCard/LinkCard";
import PlaceHolderText from "../PlaceholderText/PlaceHolderText";
import _ from "lodash";
import { Spinner } from "react-bootstrap";
import { FetchResult, useFetch } from "../../hooks/useFetch";

interface Props {
  fetchResult: FetchResult<Project[]>;
}

export const ProjectsViewStateless = (props: Props) => {
  const isLoading = props.fetchResult.isLoading;
  const hasError = !!props.fetchResult.error;
  const emptyProjectsLists =
    props.fetchResult.data && props.fetchResult.data.length === 0;

  if (isLoading) {
    return (
      <div className={styles.projectsView}>
        <Spinner
          animation="border"
          role="LoadingIndicator"
          className={styles.centered}
        >
          <span className="sr-only">Loading...</span>
        </Spinner>
      </div>
    );
  } else if (hasError) {
    return (
      <div className={styles.projectsView}>
        <span className={styles.centered}>{props.fetchResult.error}</span>
      </div>
    );
  } else if (emptyProjectsLists) {
    return (
      <div className={styles.projectsView}>
        <PlaceHolderText
          text={"No projects found"}
          className={styles.centered}
        />
      </div>
    );
  } else if (props.fetchResult.data) {
    return (
      <div className={styles.projectsView}>
        {" "}
        {_.sortBy(props.fetchResult.data, [
          (p: Project) => p.name.toLowerCase(),
        ]).map((p: Project) => {
          return (
            <div key={p.id} className={styles.projectsViewProjectComponent}>
              <LinkCard name={p.name} linkTo={`/projects/${p.id}`} />
            </div>
          );
        })}
      </div>
    );
  }
  return <></>;
};

export const ProjectsView = () => {
  const fetchResult = useFetch<Project[]>("/api/v1/projects");
  return <ProjectsViewStateless fetchResult={fetchResult} />;
};
