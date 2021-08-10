import { PageRequest } from "./Page";
import queryString from "query-string";
export function toQueryString(pageRequest: PageRequest): string {
  return queryString.stringify({
    page_number: pageRequest.page_number,
    page_size: pageRequest.page_size,
  });
}

export function fromQueryString(theQueryString: string): PageRequest {
  const parsed = queryString.parse(theQueryString, { parseNumbers: true });
  const pageNumber = Number(parsed.page_number);
  const pageSize = Number(parsed.page_size);
  if (Number.isNaN(pageNumber) || Number.isNaN(pageSize)) {
    throw new Error("Invalid query string: " + theQueryString);
  }
  return {
    page_number: pageNumber,
    page_size: pageSize,
  };
}
