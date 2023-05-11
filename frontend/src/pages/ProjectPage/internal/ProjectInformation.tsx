import React from "react";
import styles from "./ProjectInformation.module.scss";
import { useFetch } from "use-http";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
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
        <SkeletonTheme baseColor="#f7f7f7" highlightColor="white">
          <p>
            <Skeleton count={1} width={300} height={50} />
          </p>
        </SkeletonTheme>
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
