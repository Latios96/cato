import React from "react";
import styles from "./AboutComponent.module.css";
import { Spinner } from "react-bootstrap";
import { useFetch } from "../../hooks/useFetch";

interface AboutInformation {
  version: string;
}

const AboutComponent = () => {
  const { isLoading, error, data } =
    useFetch<AboutInformation>("/api/v1/about");

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
    </div>
  );
};

export default AboutComponent;
