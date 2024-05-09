import React, { useState } from "react";
import styles from "./ProjectsView.module.css";
import ProjectCard from "../ProjectCard/ProjectCard";
import PlaceHolderText from "../../../../components/PlaceholderText/PlaceHolderText";
import _ from "lodash";
import { FetchResult, useFetch } from "../../../../hooks/useFetch";
import {
  DataLoadedState,
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "../../../../components/LoadingStateHandler/LoadingStateHandler";
import ErrorMessageBox from "../../../../components/ErrorMessageBox/ErrorMessageBox";
import {
  Project,
  ProjectStatus,
} from "../../../../catoapimodels/catoapimodels";
import ArrowButton from "../../../../components/Button/ArrowButton";

interface Props {
  fetchResult: FetchResult<Project[]>;
}

function activeProjects(projects: Project[]) {
  return projects.filter((p) => p.status === ProjectStatus.ACTIVE);
}

function archivedProjects(projects: Project[]) {
  return projects.filter((p) => p.status === ProjectStatus.ARCHIVED);
}
export const ProjectsViewPresenter = (props: Props) => {
  const [archivedProjectsExpanded, setArchivedProjectsExpanded] =
    useState(false);
  const emptyProjectsLists =
    props.fetchResult.data && props.fetchResult.data.length === 0;
  return (
    <LoadingStateHandler
      isLoading={props.fetchResult.isLoading}
      error={props.fetchResult.error}
    >
      <LoadingState>
        <div className={styles.projectsViewContainer}>
          <div className={styles.projectsView}>
            {_.range(6).map((i) => {
              return (
                <div key={i} className={styles.projectsViewProjectComponent}>
                  <ProjectCard isLoading={true}></ProjectCard>
                </div>
              );
            })}
          </div>
        </div>
      </LoadingState>
      <ErrorState>
        <div className={styles.projectsView}>
          <span className={styles.centered}>
            <ErrorMessageBox
              heading={"An error occurred while loading all projects"}
              message={props.fetchResult.error?.message}
            />
          </span>
        </div>
      </ErrorState>
      <DataLoadedState>
        {props.fetchResult.data !== undefined ? (
          emptyProjectsLists ? (
            <div className={styles.projectsView}>
              <PlaceHolderText
                text={"No projects found"}
                className={styles.centered}
              />
            </div>
          ) : (
            <div className={styles.projectsViewContainer}>
              <div className={styles.projectsView}>
                {_.sortBy(activeProjects(props.fetchResult.data), [
                  (p: Project) => p.name.toLowerCase(),
                ]).map((p: Project) => {
                  return (
                    <div
                      key={p.id}
                      className={styles.projectsViewProjectComponent}
                    >
                      <ProjectCard project={p} isLoading={false} />
                    </div>
                  );
                })}
              </div>
              <div
                className={`${styles.projectsView} ${styles.archivedProjectsButton}`}
              >
                <ArrowButton
                  direction={archivedProjectsExpanded ? "down" : "right"}
                  text={"Archived Projects"}
                  onClick={() =>
                    setArchivedProjectsExpanded(!archivedProjectsExpanded)
                  }
                />
              </div>
              {archivedProjectsExpanded ? (
                <div className={styles.projectsView}>
                  {_.sortBy(archivedProjects(props.fetchResult.data), [
                    (p: Project) => p.name.toLowerCase(),
                  ]).map((p: Project) => {
                    return (
                      <div
                        key={p.id}
                        className={styles.projectsViewProjectComponent}
                      >
                        <ProjectCard project={p} isLoading={false} />
                      </div>
                    );
                  })}
                </div>
              ) : null}
            </div>
          )
        ) : null}
      </DataLoadedState>
    </LoadingStateHandler>
  );
};

export const ProjectsView = () => {
  const fetchResult = useFetch<Project[]>("/api/v1/projects");
  return <ProjectsViewPresenter fetchResult={fetchResult} />;
};
