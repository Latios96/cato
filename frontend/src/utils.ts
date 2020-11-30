import ago from "s-ago";

export function formatTime(datestr: string): string {
  var date = new Date(datestr);
  return ago(date);
}
