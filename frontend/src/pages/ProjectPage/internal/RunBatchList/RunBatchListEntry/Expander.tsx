import React from "react";
import { CaretDownFill, CaretRightFill } from "react-bootstrap-icons";

interface Props {
  isExpanded: boolean;
  onExpandToggleClick: () => void;
}

function Expander(props: Props) {
  return (
    <div
      role="button"
      aria-expanded={props.isExpanded}
      onClick={props.onExpandToggleClick}
    >
      {props.isExpanded ? (
        <CaretDownFill size={20} />
      ) : (
        <CaretRightFill size={20} />
      )}
    </div>
  );
}

export default Expander;
