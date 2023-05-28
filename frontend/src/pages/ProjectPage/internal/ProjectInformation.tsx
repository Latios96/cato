import React from "react";
import styles from "./ProjectInformation.module.scss";
import Skeleton from "react-loading-skeleton";
import { Helmet } from "react-helmet";
import { Project } from "../../../catoapimodels/catoapimodels";
interface Props {
  project: Project | undefined;
  isLoading: boolean;
}

function ProjectInformation(props: Props) {
  if (props.isLoading) {
    return (
      <div className={styles.projectInformation}>
        <div className={styles.projectInformationSkeleton}>
          <Skeleton count={1} width={350} height={30} />
        </div>
      </div>
    );
  }
  return (
    <>
      <Helmet>
        <title>{props.project?.name || "Cato"}</title>
      </Helmet>
      <div className={styles.projectInformation}>
        <h1>{props.project?.name || ""}</h1>
      </div>
    </>
  );
}

export default ProjectInformation;
