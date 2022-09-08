import React from "react";
import InfoBox from "../InfoBox/InfoBox";
import styles from "./UnsyncedEdits.module.scss";
import CopyToClipboardInput from "../CopyToClipboardInput/CopyToClipboardInput";
interface Props {
  runId: number;
  unsyncedEditCount: number;
}

function UnsyncedEdits(props: Props) {
  return (
    <InfoBox>
      <div className={styles.unsyncedEditCount}>
        <span>{props.unsyncedEditCount}</span> <span>unsynced edits</span>
      </div>
      <div className={styles.unsyncedEditCopy}>
        <CopyToClipboardInput
          clipboardText={`cato sync-edits -u ${window.location.origin} -run-id ${props.runId}`}
          tooltipText={"Copy sync command to clipboard"}
          copiedMessage={"Copied sync command!"}
        />
      </div>
    </InfoBox>
  );
}

export default UnsyncedEdits;
