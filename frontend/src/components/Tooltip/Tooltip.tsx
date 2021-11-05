import React, {
  PropsWithChildren,
  ReactElement,
  ReactNode,
  useCallback,
} from "react";
import { OverlayTrigger, Tooltip as BootstrapTooltip } from "react-bootstrap";

interface Props {
  tooltipText: string;
  tooltippedElement: ReactElement;
}

function Tooltip(props: PropsWithChildren<Props>) {
  const renderTooltip = useCallback(
    (tooltipProps: any) => (
      <BootstrapTooltip id="button-tooltip" {...tooltipProps}>
        {props.tooltipText}
      </BootstrapTooltip>
    ),
    [props.tooltipText]
  );
  return (
    <OverlayTrigger
      placement="top"
      delay={{ show: 0, hide: 0 }}
      overlay={renderTooltip}
      trigger={["hover", "focus"]}
    >
      {props.tooltippedElement}
    </OverlayTrigger>
  );
}

export default Tooltip;
