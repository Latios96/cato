import React, { useCallback } from "react";
import { OverlayTrigger, Tooltip } from "react-bootstrap";
import { QuestionCircle } from "react-bootstrap-icons";

interface Props {
  informationText: string;
}

function InformationIcon(props: Props) {
  const renderTooltip = useCallback(
    (tooltipProps: any) => (
      <Tooltip id="button-tooltip" {...tooltipProps}>
        {props.informationText}
      </Tooltip>
    ),
    [props.informationText]
  );
  return (
    <OverlayTrigger
      placement="top"
      delay={{ show: 0, hide: 150 }}
      overlay={renderTooltip}
      trigger={["hover", "focus"]}
    >
      <QuestionCircle size={16} color={"grey"} />
    </OverlayTrigger>
  );
}

export default InformationIcon;
