import ago from "s-ago";
import humanizeDuration from "humanize-duration";
import queryString from "query-string";

export function formatTime(datestr: string | null | undefined): string {
  if (!datestr) {
    return "";
  }
  datestr = datestr.replace(" GMT", "");
  var date = new Date(datestr);
  return ago(date);
}

export function formatDuration(
  durationInSeconds: number | "NaN" | undefined | null
): string {
  if (durationInSeconds == null || durationInSeconds === "NaN") {
    return "";
  }
  return humanizeDuration(durationInSeconds * 1000, { round: true });
}

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
