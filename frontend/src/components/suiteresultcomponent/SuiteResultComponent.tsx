import React, { useEffect, useState } from "react";
import { SuiteResultSummaryDto } from "../../catoapimodels";
import TestResultList from "../suiteandtestslists/TestResultList";
import TestResultBreadCrumb from "../testresultbreadcrumb/TestResultBreadCrumb";
interface Props {
  suiteId: number;
  projectId: number;
  runId: number;
}
const SuiteResultComponent = (props: Props) => {
  let [suiteResult, setSuiteResult] = useState<SuiteResultSummaryDto>();

  useEffect(() => {
    fetch(`/api/v1/suite_results/${props.suiteId}`)
      .then((res) => res.json())
      .then(
        (result) => {
          setSuiteResult(result);
        },
        (error) => {
          console.log(error);
        }
      );
  }, [props.suiteId]);

  let renderTestResult = (suiteResult: SuiteResultSummaryDto) => {
    return (
      <TestResultList
        testResults={suiteResult.tests}
        projectId={props.projectId}
        runId={props.runId}
      />
    );
  };

  return (
    <div>
      <TestResultBreadCrumb
        projectId={props.projectId}
        runId={props.runId}
        suiteId={props.suiteId}
        suiteName={suiteResult ? suiteResult.suite_name : ""}
      />
      {suiteResult ? renderTestResult(suiteResult) : <React.Fragment />}
    </div>
  );
};

export default SuiteResultComponent;
