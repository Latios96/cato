import React, { Component } from "react";
import styles from "./AboutComponent.module.css";

interface Props {}

const FRONTEND_VERSION = "0.17.2";

interface State {
  backendVersion: string;
}

class AboutComponent extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { backendVersion: "" };
  }

  componentDidMount() {
    fetch("/api/v1/about")
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ backendVersion: result.version });
        },
        (error) => {
          console.log(error);
        }
      );
  }

  render() {
    return (
      <div className={styles.about}>
        <div>
          <span>Cato Server:</span> <span>{this.state.backendVersion}</span>
        </div>
        <div>
          <span>Frontend:</span> <span>{FRONTEND_VERSION}</span>
        </div>
      </div>
    );
  }
}

export default AboutComponent;
