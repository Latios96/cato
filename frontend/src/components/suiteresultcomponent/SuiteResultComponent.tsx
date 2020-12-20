import React, { useEffect, useState } from "react";
import { SuiteResultSummaryDto } from "../../catoapimodels";
import TestResultList from "../suiteandtestslists/TestResultList";
interface Props {
  suiteId: number;
}
const SuiteResultComponent = (props: Props) => {
  let [suiteResult, setSuiteResult] = useState<SuiteResultSummaryDto>();

  useEffect(() => {
    fetch(`/api/v1/suite_results/${props.suiteId}/summary`)
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
    return <TestResultList testResults={suiteResult.tests} />;
  };

  return (
    <div>
      {suiteResult ? renderTestResult(suiteResult) : <React.Fragment />}
    </div>
  );
};

export default SuiteResultComponent;
