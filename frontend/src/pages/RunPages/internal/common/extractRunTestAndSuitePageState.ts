import { FilterOptions } from "../../../../models/FilterOptions";
import queryString from "query-string";
import { filterOptionsFromQueryString } from "../../../../utils/filterOptionUtils";

export interface State {
  currentFilterOptions: FilterOptions;
  selectedTest: number | undefined;
}

export function parseStateFromQueryString(theQueryString: string): State {
  const queryParams = queryString.parse(theQueryString, {
    parseNumbers: true,
  });

  const currentFilterOptions = filterOptionsFromQueryString(theQueryString);
  const state = {
    currentFilterOptions,
    selectedTest: undefined,
  };
  if (
    queryParams.selectedTest &&
    !Array.isArray(queryParams.selectedTest) &&
    !(typeof queryParams.selectedTest === "string")
  ) {
    return {
      ...state,
      selectedTest: queryParams.selectedTest,
    };
  }
  return state;
}
