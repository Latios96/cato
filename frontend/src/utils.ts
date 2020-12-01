import ago from "s-ago";
import humanizeDuration from "humanize-duration";

export function formatTime(datestr: string): string {
  var date = new Date(datestr);
  return ago(date);
}

export function formatDuration(durationInSeconds: number): string {
  return humanizeDuration(durationInSeconds * 1000);
}
