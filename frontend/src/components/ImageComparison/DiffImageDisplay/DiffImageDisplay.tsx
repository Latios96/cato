import React, { useState } from "react";
import { Spinner } from "react-bootstrap";
import styles from "./DiffImageDisplay.module.scss";

interface Props {
  imageUrl: string;
}

function DiffImageDisplay(props: Props) {
  const [isLoading, setLoading] = useState(true);
  return (
    <div className={styles.container}>
      <img
        src={props.imageUrl}
        onLoad={() => setLoading(false)}
        onError={() => setLoading(false)}
        style={{ display: isLoading ? "None" : "" }}
        alt={"A diff"}
      />
      {isLoading ? (
        <div className={styles.spinner}>
          <Spinner animation="border" role="status" variant={"light"}>
            <span className="sr-only">Loading...</span>
          </Spinner>
        </div>
      ) : (
        ""
      )}
      <div className={styles.diffHighlightInformation}>
        <div style={{}} /> <span>Minimal Error</span>
        <div style={{}} /> <span>Maximal Error</span>
      </div>
    </div>
  );
}

export default DiffImageDisplay;
