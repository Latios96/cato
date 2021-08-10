import { PageRequest } from "./Page";
import queryString from "query-string";
export function toQueryString(pageRequest: PageRequest): string {
  return queryString.stringify({
    page_number: pageRequest.page_number,
    page_size: pageRequest.page_size,
  });
}

export function fromQueryString(
  theQueryString: string,
  defaultPage?: PageRequest
): PageRequest {
  const parsed = queryString.parse(theQueryString, { parseNumbers: true });
  const pageNumber = Number(parsed.page_number);
  const pageSize = Number(parsed.page_size);
  const invalidData = Number.isNaN(pageNumber) || Number.isNaN(pageSize);
  if (invalidData && !defaultPage) {
    throw new Error("Invalid query string: " + theQueryString);
  } else if (invalidData && defaultPage) {
    return defaultPage;
  }
  return {
    page_number: pageNumber,
    page_size: pageSize,
  };
}
