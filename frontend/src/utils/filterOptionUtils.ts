import {
  StatusFilter,
  TestResultFilterOptions,
} from "../models/TestResultFilterOptions";
import queryString from "query-string";

export function testResultFilterOptionsFromQueryString(
  theQueryString: string
): TestResultFilterOptions {
  const parsedData = queryString.parse(theQueryString);
  if (parsedData.statusFilter && !Array.isArray(parsedData.statusFilter)) {
    return new TestResultFilterOptions(
      StatusFilter[parsedData.statusFilter as keyof typeof StatusFilter]
    );
  }
  return new TestResultFilterOptions();
}

export function testResultFilterOptionsForQueryString(
  filterOptions: TestResultFilterOptions
) {
  return {
    statusFilter: filterOptions.status,
  };
}

export function testResultFilterOptionsToQueryString(
  filterOptions: TestResultFilterOptions
) {
  return queryString.stringify(
    testResultFilterOptionsForQueryString(filterOptions)
  );
}
