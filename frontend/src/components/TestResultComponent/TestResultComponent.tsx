import React, { useCallback, useEffect, useState } from "react";
import FinishedTestResultComponent from "./FinishedTestResultComponent";
import WaitingOrRunningTestResultComponent from "./WaitingOrRunningTestResultComponent";
import TestResultBreadCrumb from "../TestResultBreadCrumb/TestResultBreadCrumb";
import { TestResultUpdateContext } from "../TestResultUpdateContext/TestResultUpdateContext";
import { TestResultDto } from "../../catoapimodels/catoapimodels";

interface Props {
  resultId: number;
  projectId: number;
  runId: number;
}

function TestResultComponent(props: Props) {
  let [result, setResult] = useState<TestResultDto>();

  const fetchTest = useCallback((id) => {
    fetch(`/api/v1/test_results/${id}`)
      .then((res) => res.json())
      .then(
        (result) => {
          setResult(result);
        },
        (error) => {}
      );
  }, []);

  useEffect(() => {
    fetchTest(props.resultId);
  }, [fetchTest, props.resultId]);

  let renderTestResult = (testResult: TestResultDto) => {
    if (
      testResult.unifiedTestStatus !== "NOT_STARTED" &&
      testResult.unifiedTestStatus !== "RUNNING"
    ) {
      return <FinishedTestResultComponent result={testResult} />;
    }
    return <WaitingOrRunningTestResultComponent result={testResult} />;
  };

  return (
    <div>
      <TestResultUpdateContext.Provider value={{ update: fetchTest }}>
        <TestResultBreadCrumb
          projectId={props.projectId}
          runId={props.runId}
          suiteId={result ? result.suiteResultId : 0}
          suiteName={result ? result.testIdentifier.split("/")[0] : ""}
          testName={result ? result.testName : ""}
        />
        {result ? renderTestResult(result) : <React.Fragment />}
      </TestResultUpdateContext.Provider>
    </div>
  );
}

export default TestResultComponent;
