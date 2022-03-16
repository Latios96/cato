import React from "react";
import { updateQueryString } from "../../../../utils/queryStringUtils";
import queryString from "query-string";
import { useHistory } from "react-router-dom";
import { useReFetch } from "../../../../hooks/useReFetch";
import { SuiteTestListImpl } from "./SuiteTestListImpl";
import {
  SuiteResultDto,
  TestResultDto,
} from "../../../../catoapimodels/catoapimodels";

interface Props {
  suite: SuiteResultDto;
}

function SuiteTestList(props: Props) {
  const { data, isLoading, error } = useReFetch<TestResultDto[]>(
    `api/v1/test_results/suite_result/${props.suite.id}`,
    5000,
    [props.suite.id]
  );
  const history = useHistory();
  const queryParams = queryString.parse(history.location.search, {
    parseNumbers: true,
  });

  const selectedTestId = queryParams.selectedTest;
  return (
    <SuiteTestListImpl
      loading={isLoading}
      error={error}
      data={data}
      selectedTestId={selectedTestId}
      onClick={(test) => {
        history.push({
          search: updateQueryString(history.location.search, {
            selectedSuite: props.suite.id,
            selectedTest: test.id,
          }),
        });
      }}
      suiteId={props.suite.id}
    />
  );
}

export default SuiteTestList;
