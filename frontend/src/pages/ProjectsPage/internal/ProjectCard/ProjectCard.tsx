import React, { useState } from "react";
import { Link } from "react-router-dom";
import styles from "./ProjectCard.module.scss";
import Skeleton from "react-loading-skeleton";
import {
  Archive,
  CheckCircle,
  Images,
  ThreeDotsVertical,
} from "react-bootstrap-icons";
import { OverlayTrigger } from "react-bootstrap";
import {
  Project,
  ProjectStatus,
} from "../../../../catoapimodels/catoapimodels";
import Spinner from "../../../../components/Spinner/Spinner";
import axios from "axios";

interface Props {
  project?: Project;
  isLoading?: boolean;
}

const ProjectCard = (props: Props) => {
  const linkTo = props.project ? `/projects/${props.project.id}` : "";
  const [actionIsRunning, setActionIsRunning] = useState(false);
  return (
    <Link to={linkTo} style={{ textDecoration: "none" }}>
      <div className={`overflow-hidden rounded ${styles.projectCard}`}>
        <div
          className={`overflow-hidden d-flex justify-content-center align-items-center ${styles.projectCardImage}`}
        >
          {props.isLoading ? (
            <Skeleton
              count={1}
              width={300}
              height={165}
              style={{ lineHeight: "inherit" }}
            />
          ) : (
            <Images className={"m-auto"} size={50} color={"grey"} />
          )}
        </div>
        <div className={"p-1 pl-2 border-top"}>
          {props.isLoading ? (
            <Skeleton count={1} width={200} height={22} />
          ) : (
            <div className={"d-flex align-items-center "}>
              <span>{props.project?.name || ""}</span>

              <OverlayTrigger
                placement={"bottom"}
                trigger={"click"}
                rootClose={true}
                overlay={
                  <div
                    id={`${props.project?.name}-menu ${props.project?.name}-menu-open`}
                    className={`rounded overflow-hidden d-flex flex-column ${styles.projectCardMenu}`}
                  >
                    <div
                      className={`p-1 pl-2 d-flex align-items-center ${styles.projectCardMenuItem}`}
                      onClick={(e) => {
                        e.preventDefault();
                        setActionIsRunning(true);
                        document.body.click();
                        axios
                          .post(
                            `/api/v1/projects/${props.project?.id}/status/${
                              props.project?.status === ProjectStatus.ACTIVE
                                ? "archived"
                                : "active"
                            }`
                          )
                          .then(() => {
                            setActionIsRunning(false);
                            window.location.reload();
                          })
                          .catch(() => {
                            setActionIsRunning(false);
                          });
                      }}
                    >
                      {props.project?.status === ProjectStatus.ACTIVE ? (
                        <>
                          <Archive />
                          <span className={"ml-2"}>Archive Project</span>
                        </>
                      ) : (
                        <>
                          <CheckCircle />
                          <span className={"ml-2"}>Activate Project</span>
                        </>
                      )}
                    </div>
                  </div>
                }
              >
                <div className={"ml-auto d-flex align-items-center"}>
                  {actionIsRunning ? (
                    <Spinner />
                  ) : (
                    <ThreeDotsVertical
                      size={19}
                      onClick={(e) => e.preventDefault()}
                    />
                  )}
                </div>
              </OverlayTrigger>
            </div>
          )}
        </div>
      </div>
    </Link>
  );
};

export default ProjectCard;
