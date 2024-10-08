import React, { PropsWithChildren, useRef, useState } from "react";
import { Link } from "react-router-dom";
import styles from "./ProjectCard.module.scss";
import Skeleton from "react-loading-skeleton";
import {
  Archive,
  CheckCircle,
  Images,
  ThreeDotsVertical,
  Upload,
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

interface MenuItemProps {
  onClick: () => void;
}

const MenuItem = (props: PropsWithChildren<MenuItemProps>) => {
  return (
    <div
      className={`p-1 pl-2 d-flex align-items-center ${styles.projectCardMenuItem}`}
      onClick={(e) => {
        e.preventDefault();
        props.onClick();
      }}
    >
      {props.children}
    </div>
  );
};

const ProjectCard = (props: Props) => {
  const linkTo = props.project ? `/projects/${props.project.id}` : "";
  const [actionIsRunning, setActionIsRunning] = useState(false);
  const inputFile = useRef<HTMLInputElement>(null);

  return (
    <>
      <input
        type={"file"}
        ref={inputFile}
        className={"d-none"}
        onChange={(event) => {
          event.stopPropagation();
          event.preventDefault();
          if (event.target.files) {
            var file = event.target.files[0];
            setActionIsRunning(true);
            // eslint-disable-next-line no-console
            console.log(file);
            const formData = new FormData();
            formData.append("file", file);
            axios
              .post(
                `/api/v1/projects/${props.project?.id}/uploadImage`,
                formData
              )
              .then(() => {
                setActionIsRunning(false);
                window.location.reload();
              })
              .catch(() => {
                setActionIsRunning(false);
              });
          }
        }}
      />
      <Link
        to={linkTo}
        style={{ textDecoration: "none" }}
        id={`project-card-${props.project?.id}`}
      >
        <div className={`${styles.projectCard} overflow-hidden rounded `}>
          <div
            className={`${styles.projectCardImage} overflow-hidden d-flex justify-content-center align-items-center `}
          >
            {props.isLoading ? (
              <Skeleton
                count={1}
                width={300}
                height={165}
                style={{ lineHeight: "inherit" }}
              />
            ) : props.project?.thumbnailFileId ? (
              <img
                alt={"project"}
                className={"w-100 object-fit-cover"}
                src={`/api/v1/files/${props.project.thumbnailFileId}`}
                style={
                  props.project.status === ProjectStatus.ARCHIVED
                    ? { filter: "grayscale(1)" }
                    : {}
                }
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
                      className={`${styles.projectCardMenu} rounded overflow-hidden d-flex flex-column `}
                    >
                      <MenuItem
                        onClick={() => {
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
                      </MenuItem>
                      <MenuItem
                        onClick={() => {
                          if (inputFile.current) {
                            inputFile.current.click();
                          }
                        }}
                      >
                        <Upload />
                        <span className={"ml-1"}> Upload Project Image</span>
                      </MenuItem>
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
    </>
  );
};

export default ProjectCard;
