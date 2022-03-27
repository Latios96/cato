export function isLast(index: number, arr: any[]) {
  return index + 1 === arr.length;
}

export function isNotLast(index: number, arr: any[]) {
  return !isLast(index, arr);
}
