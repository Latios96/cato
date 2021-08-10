import React from "react";
import styles from "./SideBar.module.scss";
import { Link } from "react-router-dom";
import { CurrentPage } from "./CurrentPage";
import { ChevronLeft } from "react-bootstrap-icons";
interface Props {
  currentPage: CurrentPage;
  projectId: number;
  runId: number;
}

function SideBar(props: Props) {
  return (
    <div
      className={
        "d-flex flex-column flex-shrink-0 p-3 text-white " + styles.sideMenu
      }
      id={"sidebar"}
    >
      <ul className={`nav nav-pills flex-column mb-aut o`}>
        <li>
          <Link to={`/projects/${props.projectId}`}>
            <ChevronLeft style={{ marginTop: "-3px" }} /> Back to Project
          </Link>
        </li>
        <li
          className={
            props.currentPage === CurrentPage.OVERVIEW ? styles.active : ""
          }
        >
          <Link to={`/projects/${props.projectId}/runs/${props.runId}`}>
            Overview
          </Link>
        </li>
        <li
          className={
            props.currentPage === CurrentPage.SUITES ? styles.active : ""
          }
        >
          <Link to={`/projects/${props.projectId}/runs/${props.runId}/suites`}>
            Suites
          </Link>
        </li>
        <li
          className={
            props.currentPage === CurrentPage.TESTS ? styles.active : ""
          }
        >
          <Link to={`/projects/${props.projectId}/runs/${props.runId}/tests`}>
            Tests
          </Link>
        </li>
      </ul>
    </div>
  );
}

export default SideBar;
