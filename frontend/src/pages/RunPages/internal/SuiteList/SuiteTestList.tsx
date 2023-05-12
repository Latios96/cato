import React from "react";
import { updateQueryString } from "../../../../utils/queryStringUtils";
import queryString from "query-string";
import { useHistory } from "react-router-dom";
import { SuiteResultSummaryDto } from "../../../../catoapimodels/catoapimodels";
import styles from "./SuiteListEntry.module.scss";
import TestStatus from "../../../../components/Status/TestStatus";
import { Thumbnail } from "../../../../components/Thumbnail/Thumbnail";
import { toHoursAndMinutes } from "../../../../utils/dateUtils";

interface Props {
  suite: SuiteResultSummaryDto;
}

function SuiteTestList(props: Props) {
  const history = useHistory();
  const queryParams = queryString.parse(history.location.search, {
    parseNumbers: true,
  });

  const selectedTestId = queryParams.selectedTest;
  return (
    <div className={styles.suiteListEntryContent}>
      {props.suite.tests.length === 0 ? (
        <div>
          <span>This suite has no tests</span>
        </div>
      ) : null}
      {props.suite.tests.map((test) => {
        return (
          <div
            onClick={(e) => {
              history.push({
                search: updateQueryString(history.location.search, {
                  selectedSuite: props.suite.id,
                  selectedTest: test.id,
                }),
              });
            }}
            className={selectedTestId === test.id ? styles.active : ""}
            id={`suite-${props.suite.id}-test-${test.id}`}
          >
            <span>
              <TestStatus testResult={test} />
            </span>
            <span>
              <Thumbnail
                url={
                  test.thumbnailFileId
                    ? `/api/v1/files/${test.thumbnailFileId}`
                    : undefined
                }
                width={"55px"}
                height={"30px"}
              />
            </span>
            <span>{test.name}</span>
            <span>{toHoursAndMinutes(test.seconds || 0)}</span>
          </div>
        );
      })}
    </div>
  );
}

export default SuiteTestList;
