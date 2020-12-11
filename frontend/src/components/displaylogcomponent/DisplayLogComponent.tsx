import React, { Component } from "react";
import LogComponent from "../logcomponent/LogComponent";
import { Button } from "react-bootstrap";

interface Props {
  testResultId: number;
}

interface State {
  isOpened: boolean;
  content: string;
  contentIsLoaded: boolean;
}

class DisplayLogComponent extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { isOpened: false, content: "", contentIsLoaded: false };
  }

  render() {
    return (
      <div>
        <Button onClick={(e) => this.toggle()}>
          {this.state.isOpened ? "Hide Log" : "Display Log"}
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
    fetch(`api/v1/test_results/${this.props.testResultId}/output`)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ content: result.text, contentIsLoaded: true });
        },
        (error) => {
          console.log(error);
        }
      );
  };
}

export default DisplayLogComponent;
