import React from "react";
import { formatTime } from "../../utils/dateUtils";
import Tooltip from "../Tooltip/Tooltip";
import { format } from "date-fns";

interface Props {
  datestr: string | null | undefined;
}

function FormattedTime(props: Props) {
  if (!props.datestr) {
    return <></>;
  }
  return (
    <Tooltip
      tooltipText={format(new Date(props.datestr), "MMM do, yyyy HH:mm OOOO")}
      tooltippedElement={<span>{formatTime(props.datestr)}</span>}
    />
  );
}

export default FormattedTime;
