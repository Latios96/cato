import queryString from "query-string";

export function updateQueryString(theQueryString: string, data: object) {
  const parsedData = queryString.parse(theQueryString);
  Object.assign(parsedData, data);
  return queryString.stringify(parsedData);
}

export function popFromQueryString(theQueryString: string, keys: string[]) {
  const parsedData = queryString.parse(theQueryString);
  keys.forEach((key) => {
    delete parsedData[key];
  });
  return queryString.stringify(parsedData);
}
