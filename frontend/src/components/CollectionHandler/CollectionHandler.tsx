import React, { PropsWithChildren } from "react";

interface Props<T> {
  data?: T[];
  placeHolder: JSX.Element;
  renderElements: (data: T[]) => JSX.Element[];
}

export const CollectionHandler = <T,>(props: PropsWithChildren<Props<T>>) => {
  return (
    <>
      {props.data && props.data.length > 0
        ? props.renderElements(props.data)
        : props.placeHolder}
    </>
  );
};
