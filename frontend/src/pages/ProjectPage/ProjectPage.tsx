import React from "react";
import BasicPage from "../BasicPage";
import ProjectInformation from "./internal/ProjectInformation";
import RunBatchList from "./internal/RunBatchList/RunBatchList";
import styles from "./ProjectPage.module.scss";
interface Props {
  projectId: number;
}

function ProjectPage(props: Props) {
  return (
    <BasicPage>
      <div className={styles.projectPageScroll}>
        <ProjectInformation projectId={props.projectId} />
        <div
          className={"ml-auto mr-auto "}
          style={{ width: "850px", marginTop: "35px" }}
        ></div>
        <RunBatchList projectId={props.projectId} />
      </div>
    </BasicPage>
  );
}

export default ProjectPage;
