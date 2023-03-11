import ago from "s-ago";
import humanizeDuration from "humanize-duration";

export function formatTime(datestr: string | null | undefined): string {
  if (!datestr) {
    return "";
  }
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

export function toHoursAndMinutes(durationInSeconds: number) {
  const totalMinutes = Math.floor(durationInSeconds / 60);

  const seconds = durationInSeconds % 60;
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;

  let result = "";
  if (hours) {
    result += `${hours.toFixed(0)}h`;
  }

  if (minutes) {
    result += ` ${minutes.toFixed(0)}min`;
  }

  if (seconds) {
    const fractionDigits = seconds < 1 ? 1 : 0;
    result += ` ${seconds.toFixed(fractionDigits)}s`;
  }

  return result.trim();
}
