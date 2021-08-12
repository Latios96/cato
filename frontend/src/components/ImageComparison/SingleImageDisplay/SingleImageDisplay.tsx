import React, { FunctionComponent, useState } from "react";
import { Spinner } from "react-bootstrap";
import styles from "./SingleImageDisplay.module.scss";

interface Props {
  imageUrl: string;
  informationText: string;
}

const SingleImageDisplay: FunctionComponent<Props> = (props) => {
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
      <span className={styles.informationText}>{props.informationText}</span>
      {props.children}
    </div>
  );
};

export default SingleImageDisplay;