import React, { Component } from "react";
import styles from "./ImageComparison.module.css";
import ReactCompareImage from "react-compare-image";
import { Spinner } from "react-bootstrap";

interface Props {
  outputImageUrl: string;
  referenceImageUrl: string;
  width: number;
  height: number;
}

interface State {
  referenceImageLoaded: boolean;
  outputImageLoaded: boolean;
}

class ImageComparison extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { referenceImageLoaded: false, outputImageLoaded: false };
  }

  componentDidUpdate(
    prevProps: Readonly<Props>,
    prevState: Readonly<State>,
    snapshot?: any
  ) {
    if (
      this.props.referenceImageUrl !== prevProps.referenceImageUrl ||
      this.props.outputImageUrl !== prevProps.outputImageUrl
    ) {
      this.setState({ referenceImageLoaded: false, outputImageLoaded: false });
    }
  }

  render() {
    return (
      <div
        className={styles.imgCompContainer}
        style={{ maxWidth: this.props.width }}
      >
        <img
          src={this.props.referenceImageUrl}
          className={styles.imageSizeCalculator}
          alt={"left"}
          onLoad={() => this.setState({ referenceImageLoaded: true })}
        />
        <img
          src={this.props.outputImageUrl}
          className={styles.imageSizeCalculator}
          alt={"left"}
          onLoad={() => this.setState({ outputImageLoaded: true })}
        />
        {this.state.outputImageLoaded && this.state.referenceImageLoaded ? (
          <ReactCompareImage
            leftImage={this.props.outputImageUrl}
            rightImage={this.props.referenceImageUrl}
          />
        ) : (
          <div className={styles.spinner}>
            <Spinner animation="border" role="status">
              <span className="sr-only">Loading...</span>
            </Spinner>
          </div>
        )}
      </div>
    );
  }
}

export default ImageComparison;
