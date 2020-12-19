import React, { useEffect, useState } from "react";
import TestResult from "../../models/TestResult";
import FinishedTestResultComponent from "./FinishedTestResultComponent";
import WaitingOrRunningTestResultComponent from "./WaitingOrRunningTestResultComponent";

interface Props {
  resultId: number;
}

function TestResultComponent(props: Props) {
  let [result, setResult] = useState<TestResult>();

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

  let renderTestResult = (testResult: TestResult) => {
    if (testResult.execution_status === "FINISHED") {
      return <FinishedTestResultComponent result={testResult} />;
    }
    return <WaitingOrRunningTestResultComponent result={testResult} />;
  };

  return <div>{result ? renderTestResult(result) : <React.Fragment />}</div>;
}

export default TestResultComponent;
