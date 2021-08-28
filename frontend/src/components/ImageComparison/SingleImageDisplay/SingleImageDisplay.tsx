import React, { FunctionComponent, useState } from "react";
import { Spinner } from "react-bootstrap";
import styles from "./SingleImageDisplay.module.scss";
import {
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "../../LoadingStateHandler/LoadingStateHandler";
import { CardImage } from "react-bootstrap-icons";
interface Props {
  imageUrl: string;
  informationText: string;
}

const SingleImageDisplay: FunctionComponent<Props> = (props) => {
  const [isLoading, setLoading] = useState(true);
  const [hasError, setError] = useState(false);
  return (
    <div className={styles.container}>
      <img
        src={props.imageUrl}
        onLoad={() => setLoading(false)}
        onError={(error) => {
          setLoading(false);
          setError(true);
        }}
        style={{ display: isLoading || hasError ? "None" : "" }}
        alt={"A diff"}
      />
      <LoadingStateHandler
        isLoading={isLoading}
        error={hasError ? new Error() : undefined}
      >
        <LoadingState>
          <div className={styles.spinner}>
            <Spinner animation="border" role="status" variant={"light"}>
              <span className="sr-only">Loading...</span>
            </Spinner>
          </div>
        </LoadingState>
        <ErrorState>
          <span className={styles.errorPlaceholder}>
            <CardImage size={160} color={"#e7e7e7"} />
          </span>
        </ErrorState>
      </LoadingStateHandler>
      <span className={styles.informationText}>{props.informationText}</span>
      {props.children}
    </div>
  );
};

export default SingleImageDisplay;
