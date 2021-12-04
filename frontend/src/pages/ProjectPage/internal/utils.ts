export function toCommaSeparatedString(strings: Set<string>) {
  if (strings.size === 0) {
    return "";
  }
  return Array.from(strings).sort().join(",");
}

export function fromCommaSeparatedString(theString: string) {
  return new Set(theString.split(","));
}
