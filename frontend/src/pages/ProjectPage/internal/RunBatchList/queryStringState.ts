import queryString from "query-string";
import {
  PageRequest,
  requestFirstPageOfSize,
} from "../../../../components/Pagination/Page";
import { fromCommaSeparatedString } from "../utils";
interface State {
  page: PageRequest;
  branches: Set<string>;
}
export function parseStateFromQueryString(theQueryString: string): State {
  const queryParams = queryString.parse(theQueryString, {
    parseNumbers: true,
  });
  const state = {
    page: requestFirstPageOfSize(25),
    branches: new Set<string>(),
  };

  if (queryParams.pageNumber && queryParams.pageSize) {
    state.page.pageSize = Number(queryParams.pageSize);
    state.page.pageNumber = Number(queryParams.pageNumber);
  }
  if (queryParams.branches) {
    state.branches = fromCommaSeparatedString("" + queryParams.branches);
  }
  return state;
}
