import ago from "s-ago";
import humanizeDuration from "humanize-duration";

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
  if (durationInSeconds > 0 && durationInSeconds < 1) {
    return "less than one second";
  }
  return humanizeDuration(durationInSeconds * 1000, { round: true });
}
