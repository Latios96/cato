import React, { PropsWithChildren } from "react";

interface Props {
  title: string;
}

function WrapTitle(props: PropsWithChildren<Props>) {
  return (
    <span className="d-inline-block" data-toggle="tooltip" title={props.title}>
      {props.children}
    </span>
  );
}

export default WrapTitle;
