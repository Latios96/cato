import React from "react";
import { ChevronDown, ChevronRight } from "react-bootstrap-icons";
import SuiteStatus from "../../../components/Status/SuiteStatus";
import styles from "./SuiteListEntry.module.scss";
import { SuiteResultDto } from "../../../catoapimodels";
import { useToggle } from "rooks";
interface Props {
  suite: SuiteResultDto;
  projectId: number;
  runId: number;
}

function SuiteListEntry(props: Props) {
  const [expanded, toggle] = useToggle(false);
  return (
    <div>
      <div className={styles.suiteListEntry}>
        <span onClick={toggle}>
          {expanded ? <ChevronDown /> : <ChevronRight />}
        </span>
        <span>
          <SuiteStatus suiteResult={props.suite} />
        </span>
        <span>{props.suite.suite_name}</span>
      </div>
      <div>
        {expanded ? (
          <div className={styles.suiteListEntryContent}>
            <div>
              <span>testname</span>
            </div>
            <div>
              <span>testname</span>
            </div>
            <div>
              <span>testname</span>
            </div>
            <div>
              <span>testname</span>
            </div>
          </div>
        ) : (
          ""
        )}
      </div>
    </div>
  );
}

export default SuiteListEntry;
