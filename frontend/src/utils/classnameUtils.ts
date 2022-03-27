export function joinClassnames(names: (string | any)[]) {
  return names
    .filter((s) => s)
    .filter((s) => s.constructor === String)
    .join(" ");
}
