import React from "react";
export function renderIf<T>(
  value: T | null | undefined,
  renderCallback: (value: T) => JSX.Element
): JSX.Element {
  if (value !== undefined && value !== null) {
    return renderCallback(value);
  }
  return <React.Fragment />;
}
