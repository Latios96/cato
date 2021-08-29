import queryString from "query-string";
import { FilterOptions, StatusFilter } from "../models/FilterOptions";

export function filterOptionsFromQueryString(
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

export function filterOptionsForQueryString(filterOptions: FilterOptions) {
  return {
    statusFilter: filterOptions.status,
  };
}

export function filterOptionsToQueryString(filterOptions: FilterOptions) {
  return queryString.stringify(filterOptionsForQueryString(filterOptions));
}
