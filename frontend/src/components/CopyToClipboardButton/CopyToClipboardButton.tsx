import React, { useCallback, useState } from "react";
import { Button, OverlayTrigger, Tooltip } from "react-bootstrap";
import styles from "./CopyToClipboardButton.module.css";
import { Clipboard, ClipboardCheck } from "react-bootstrap-icons";
interface Props {
  tooltipText: string;
  clipboardText: string;
  copiedMessage: string;
}
const CopyToClipboardButton = (props: Props) => {
  const [displayCheck, setDisplayCheck] = useState(false);
  const renderTooltip = useCallback(
    (tooltipProps: any) => (
      <Tooltip id="button-tooltip" {...tooltipProps}>
        {props.copiedMessage}
      </Tooltip>
    ),
    [props.copiedMessage]
  );
  return (
    <OverlayTrigger
      placement="top"
      delay={{ show: 250, hide: 800 }}
      overlay={renderTooltip}
      trigger={["click", "focus"]}
      onToggle={(isShown) => {
        if (!isShown) {
          setDisplayCheck(false);
        }
      }}
    >
      <Button
        className={styles.buttonNoShadowOnFocus}
        onClick={(e) => {
          const icon = e.target as HTMLElement;
          if (icon.parentElement) {
            icon.parentElement.blur();
          }
          navigator.clipboard.writeText(props.clipboardText);
          setDisplayCheck(true);
        }}
        variant={"link"}
        style={{ padding: "0px" }}
        title={props.tooltipText}
      >
        {displayCheck ? <ClipboardCheck size={16} /> : <Clipboard size={16} />}
      </Button>
    </OverlayTrigger>
  );
};

CopyToClipboardButton.propTypes = {};

export default CopyToClipboardButton;
