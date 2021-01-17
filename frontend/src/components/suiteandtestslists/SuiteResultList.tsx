import React from "react";
import { Link } from "react-router-dom";
import { ListGroup } from "react-bootstrap";
import styles from "./SuiteAndTestLists.module.scss";
import { SuiteResultDto } from "../../catoapimodels";
import SuiteStatus from "../status/SuiteStatus";
import PlaceHolderText from "../placeholdertext/PlaceHolderText";

interface Props {
  suiteResults: SuiteResultDto[];
  projectId: number;
  runId: number;
}

const SuiteResultList = (props: Props) => {
  let renderPlaceholder = () => {
    return (
      <div className={styles.placeholderContainer}>
        <PlaceHolderText
          text={"No suites found"}
          className={styles.placeholder}
        />
      </div>
    );
  };

  let renderList = () => {
    return (
      <ListGroup>
        {props.suiteResults.map((suite) => {
          return (
            <Link
              to={`/projects/${props.projectId}/runs/${props.runId}/suites/${suite.id}`}
            >
              <ListGroup.Item className={styles.listEntry}>
                <span className={styles.statusInList}>
                  <SuiteStatus suiteResult={suite} />
                </span>
                <span className={styles.nameInList}>{suite.suite_name}</span>
              </ListGroup.Item>
            </Link>
          );
        })}
      </ListGroup>
    );
  };

  if (props.suiteResults.length === 0) {
    return renderPlaceholder();
  }
  return renderList();
};

export default SuiteResultList;
