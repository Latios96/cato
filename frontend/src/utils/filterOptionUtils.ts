import queryString from "query-string";
import { FilterOptions } from "../models/FilterOptions";
import {
  StatusFilter,
  TestFailureReason,
} from "../catoapimodels/catoapimodels";

export function filterOptionsFromQueryString(
  theQueryString: string
): FilterOptions {
  const parsedData = queryString.parse(theQueryString);
  let filterOptions = new FilterOptions();
  if (parsedData.statusFilter && !Array.isArray(parsedData.statusFilter)) {
    filterOptions = filterOptions.withChangedStatusFilter(
      StatusFilter[parsedData.statusFilter as keyof typeof StatusFilter]
    );
  }
  if (
    parsedData.failureReasonFilter &&
    !Array.isArray(parsedData.statusFilter) &&
    filterOptions.status === StatusFilter.FAILED
  ) {
    filterOptions = filterOptions.withChangedFailureReason(
      TestFailureReason[
        parsedData.failureReasonFilter as keyof typeof TestFailureReason
      ]
    );
  }
  return filterOptions;
}

export function filterOptionsForQueryString(filterOptions: FilterOptions) {
  return {
    statusFilter: filterOptions.status,
    failureReasonFilter: filterOptions.failureReason,
  };
}

export function filterOptionsToQueryString(filterOptions: FilterOptions) {
  return queryString.stringify(filterOptionsForQueryString(filterOptions));
}
