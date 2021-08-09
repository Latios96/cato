import React, { Component } from "react";
import LogComponent from "../LogComponent/LogComponent";
import { Button } from "react-bootstrap";
import styles from "./DisplayLogComponent.module.scss";
interface Props {
  testResultId: number;
}

interface State {
  isOpened: boolean;
  content: string;
  contentIsLoaded: boolean;
  isLoading: boolean;
}

class DisplayLogComponent extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      isOpened: false,
      content: "",
      contentIsLoaded: false,
      isLoading: false,
    };
  }

  render() {
    return (
      <div>
        <Button
          onClick={(e) => this.toggle()}
          disabled={this.state.isLoading}
          className={styles.logButton}
        >
          {this.getButtonText()}
        </Button>
        {this.state.isOpened && this.state.contentIsLoaded ? (
          <LogComponent content={this.state.content} />
        ) : (
          <React.Fragment />
        )}
      </div>
    );
  }

  toggle = () => {
    let isOpened = !this.state.isOpened;
    this.setState({ isOpened: isOpened });
    if (isOpened) {
      this.fetchLog();
    }
  };
  fetchLog = () => {
    this.setState({ isLoading: true });
    fetch(`api/v1/test_results/${this.props.testResultId}/output`)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            content: result.text,
            contentIsLoaded: true,
            isLoading: false,
          });
        },
        (error) => {
          this.setState({ isLoading: false });
        }
      );
  };
  getButtonText = () => {
    if (this.state.isLoading) {
      return "Loading..";
    }
    return this.state.isOpened ? "Hide Log" : "Display Log";
  };
}

export default DisplayLogComponent;
