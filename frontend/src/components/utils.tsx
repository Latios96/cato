import React from "react";
export function renderIf<T>(
  value: T,
  renderCallback: (value: T) => JSX.Element
): JSX.Element {
  if (value) {
    return renderCallback(value);
  }
  return <React.Fragment />;
}
