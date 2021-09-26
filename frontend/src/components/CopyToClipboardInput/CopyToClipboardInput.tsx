import React from "react";
import styles from "./CopyToClipboardInput.module.scss";
import CopyToClipboardButton from "../CopyToClipboardButton/CopyToClipboardButton";

interface Props {
  tooltipText: string;
  clipboardText: string;
  copiedMessage: string;
}

function CopyToClipboardInput(props: Props) {
  return (
    <div className={styles.copyText}>
      <input
        type={"text"}
        value={props.clipboardText}
        title={"Run this command to sync test edits locally"}
        onClick={(e) => e.currentTarget.select()}
      />
      <div className={styles.copyTextButton}>
        <CopyToClipboardButton
          tooltipText={props.tooltipText}
          clipboardText={props.clipboardText}
          copiedMessage={props.copiedMessage}
        />
      </div>
    </div>
  );
}

export default CopyToClipboardInput;
