import { PageRequest } from "./Page";
import queryString from "query-string";
export function toQueryString(pageRequest: PageRequest): string {
  return queryString.stringify({
    pageNumber: pageRequest.pageNumber,
    pageSize: pageRequest.pageSize,
  });
}

export function fromQueryString(
  theQueryString: string,
  defaultPage?: PageRequest
): PageRequest {
  const parsed = queryString.parse(theQueryString, { parseNumbers: true });
  const pageNumber = Number(parsed.pageNumber);
  const pageSize = Number(parsed.pageSize);
  const invalidData = Number.isNaN(pageNumber) || Number.isNaN(pageSize);
  if (invalidData && !defaultPage) {
    throw new Error("Invalid query string: " + theQueryString);
  } else if (invalidData && defaultPage) {
    return defaultPage;
  }
  return {
    pageNumber: pageNumber,
    pageSize: pageSize,
  };
}
