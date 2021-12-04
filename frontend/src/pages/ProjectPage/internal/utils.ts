export function toCommaSeparatedString(strings: Set<string>) {
  return Array.from(strings).sort().join(",");
}

export function fromCommaSeparatedString(theString: string) {
  return new Set(theString.split(","));
}
