import React from "react";
import { useQuery } from "react-query";
import styles from "./AboutComponent.module.css";
import { Spinner } from "react-bootstrap";

const FRONTEND_VERSION = "0.31.0";

interface AboutInformation {
  version: string;
}

const AboutComponent = () => {
  const { isLoading, error, data } = useQuery<AboutInformation, string>(
    "about",
    () => fetch("/api/v1/about").then((res) => res.json())
  );

  if (isLoading)
    return (
      <Spinner animation="border" role="status">
        <span className="sr-only">Loading...</span>
      </Spinner>
    );

  if (error) return <div>{"An error has occurred: " + error}</div>;

  if (!data) return <div>Error occurred, data is undefined</div>;

  return (
    <div className={styles.about}>
      <div>
        <span>Cato Server:</span> <span>{data.version}</span>
      </div>
      <div>
        <span>Frontend:</span> <span>{FRONTEND_VERSION}</span>
      </div>
    </div>
  );
};

export default AboutComponent;
