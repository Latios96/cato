import React from "react";
import { CaretDownFill, CaretRightFill } from "react-bootstrap-icons";

interface Props {
  isExpanded: boolean;
  onExpandToggleClick: () => void;
}

function Expander(props: Props) {
  return (
    <div className={"mr-2"}>
      {props.isExpanded ? (
        <CaretDownFill size={20} onClick={props.onExpandToggleClick} />
      ) : (
        <CaretRightFill size={20} onClick={props.onExpandToggleClick} />
      )}
    </div>
  );
}

export default Expander;
