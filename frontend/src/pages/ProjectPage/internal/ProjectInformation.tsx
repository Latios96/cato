import React from "react";
import styles from "./ProjectInformation.module.scss";
import { useFetch } from "use-http";
import Skeleton from "react-loading-skeleton";
import { Helmet } from "react-helmet";
import { Project } from "../../../catoapimodels/catoapimodels";
interface Props {
  projectId: number;
}

function ProjectInformation(props: Props) {
  const { loading, data } = useFetch<Project>(
    "/api/v1/projects/" + props.projectId,
    []
  );
  if (loading) {
    return (
      <div className={styles.projectInformation}>
        <p>
          <Skeleton count={1} width={300} height={50} />
        </p>
      </div>
    );
  }
  return (
    <>
      <Helmet>
        <title>{data ? data.name : "Cato"}</title>
      </Helmet>
      <div className={styles.projectInformation}>
        <h1>{data ? data.name : ""}</h1>
      </div>
    </>
  );
}

export default ProjectInformation;
