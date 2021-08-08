import React, { FunctionComponent } from "react";
import { useToggle } from "rooks";
import { ChevronRight, ChevronDown } from "react-bootstrap-icons";

interface Props {}

export const ExpandingListEntry: FunctionComponent<Props> = (props) => {
  const [isExpanded, toggleExpanded] = useToggle(false);
  return (
    <div onClick={toggleExpanded}>
      {isExpanded ? <ChevronDown /> : <ChevronRight />}
    </div>
  );
};

export default ExpandingListEntry;
