import React from "react";
import { ChevronDown, ChevronRight } from "react-bootstrap-icons";
import SuiteStatus from "../../../../components/Status/SuiteStatus";
import styles from "./SuiteListEntry.module.scss";
import { useToggle } from "rooks";

import { useHistory } from "react-router-dom";

import {
  popFromQueryString,
  updateQueryString,
} from "../../../../utils/queryStringUtils";
import SuiteTestList from "./SuiteTestList";
import queryString from "query-string";
import { SuiteResultDto } from "../../../../catoapimodels/catoapimodels";
import Skeleton from "react-loading-skeleton";

interface Props {
  suite: SuiteResultDto;
  projectId: number;
  runId: number;
}

export function SuiteListEntry(props: Props) {
  const history = useHistory();
  const [expanded, toggle] = useToggle(false);

  const toggleExpansion = () => {
    let search = "";
    if (!expanded) {
      search = updateQueryString(history.location.search, {
        selectedSuite: props.suite.id,
      });
    } else {
      search = popFromQueryString(history.location.search, ["selectedSuite"]);
    }
    history.push({
      search,
    });
    toggle(true);
  };

  const queryParams = queryString.parse(history.location.search, {
    parseNumbers: true,
  });

  const selectedSuiteId = queryParams.selectedSuite;
  if (selectedSuiteId === props.suite.id && !expanded) {
    toggle(true);
  }

  return (
    <div>
      <div
        className={styles.suiteListEntry}
        id={`suiteListEntry${props.suite.id}`}
      >
        <span onClick={toggleExpansion} id={`toggleSuite${props.suite.id}Icon`}>
          {expanded ? <ChevronDown /> : <ChevronRight />}
        </span>
        <span>
          <SuiteStatus suiteResult={props.suite} />
        </span>
        <span>{props.suite.suiteName}</span>
      </div>
      <div>{expanded ? <SuiteTestList suite={props.suite} /> : ""}</div>
    </div>
  );
}

export function SuiteListEntrySkeleton() {
  return (
    <div>
      <div className={styles.suiteListEntry}>
        <span>
          <ChevronRight />
        </span>
        <span>
          <Skeleton width={27} height={27} />
        </span>
        <span>
          <Skeleton width={100} height={27} />
        </span>
      </div>
    </div>
  );
}
