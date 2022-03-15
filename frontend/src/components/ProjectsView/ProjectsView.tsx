import React from "react";
import styles from "./ProjectsView.module.css";
import LinkCard from "../LinkCard/LinkCard";
import PlaceHolderText from "../PlaceholderText/PlaceHolderText";
import _ from "lodash";
import { Spinner } from "react-bootstrap";
import { FetchResult, useFetch } from "../../hooks/useFetch";
import {
  DataLoadedState,
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "../LoadingStateHandler/LoadingStateHandler";
import ErrorMessageBox from "../ErrorMessageBox/ErrorMessageBox";
import { Project } from "../../catoapimodels/catoapimodels";

interface Props {
  fetchResult: FetchResult<Project[]>;
}

export const ProjectsViewPresenter = (props: Props) => {
  const emptyProjectsLists =
    props.fetchResult.data && props.fetchResult.data.length === 0;
  return (
    <LoadingStateHandler
      isLoading={props.fetchResult.isLoading}
      error={props.fetchResult.error}
    >
      <LoadingState>
        <div className={styles.projectsView}>
          <Spinner
            animation="border"
            role="LoadingIndicator"
            className={styles.centered}
          >
            <span className="sr-only">Loading...</span>
          </Spinner>
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
            <div className={styles.projectsView}>
              {_.sortBy(props.fetchResult.data, [
                (p: Project) => p.name.toLowerCase(),
              ]).map((p: Project) => {
                return (
                  <div
                    key={p.id}
                    className={styles.projectsViewProjectComponent}
                  >
                    <LinkCard name={p.name} linkTo={`/projects/${p.id}`} />
                  </div>
                );
              })}
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
