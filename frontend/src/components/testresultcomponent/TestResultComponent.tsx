import React, { useEffect, useState } from "react";
import FinishedTestResultComponent from "./FinishedTestResultComponent";
import WaitingOrRunningTestResultComponent from "./WaitingOrRunningTestResultComponent";
import { TestResultDto } from "../../catoapimodels";
import { Breadcrumb } from "react-bootstrap";
import TestResultBreadCrumb from "../testresultbreadcrumb/TestResultBreadCrumb";

interface Props {
  resultId: number;
  projectId: number;
  runId: number;
  suiteId: number;
  suiteName: string;
}

function TestResultComponent(props: Props) {
  let [result, setResult] = useState<TestResultDto>();

  useEffect(() => {
    fetch(`/api/v1/test_results/${props.resultId}`)
      .then((res) => res.json())
      .then(
        (result) => {
          setResult(result);
        },
        (error) => {
          console.log(error);
        }
      );
  }, [props.resultId]);

  let renderTestResult = (testResult: TestResultDto) => {
    if (testResult.execution_status === "FINISHED") {
      return <FinishedTestResultComponent result={testResult} />;
    }
    return <WaitingOrRunningTestResultComponent result={testResult} />;
  };

  return (
    <div>
      <TestResultBreadCrumb
        projectId={props.projectId}
        runId={props.runId}
        suiteId={props.suiteId}
        suiteName={props.suiteName}
        testName={result ? result.test_name : ""}
      />
      {result ? renderTestResult(result) : <React.Fragment />}
    </div>
  );
}

export default TestResultComponent;
