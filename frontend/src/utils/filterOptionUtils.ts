import { StatusFilter, FilterOptions } from "../models/FilterOptions";
import queryString from "query-string";

export function testResultFilterOptionsFromQueryString(
  theQueryString: string
): FilterOptions {
  const parsedData = queryString.parse(theQueryString);
  if (parsedData.statusFilter && !Array.isArray(parsedData.statusFilter)) {
    return new FilterOptions(
      StatusFilter[parsedData.statusFilter as keyof typeof StatusFilter]
    );
  }
  return new FilterOptions();
}

export function testResultFilterOptionsForQueryString(
  filterOptions: FilterOptions
) {
  return {
    statusFilter: filterOptions.status,
  };
}

export function testResultFilterOptionsToQueryString(
  filterOptions: FilterOptions
) {
  return queryString.stringify(
    testResultFilterOptionsForQueryString(filterOptions)
  );
}
