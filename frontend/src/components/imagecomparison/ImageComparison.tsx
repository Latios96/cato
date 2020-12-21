import React, { Component } from "react";
import styles from "./ImageComparison.module.css";
import ReactCompareImage from "react-compare-image";

interface Props {
  outputImageUrl: string;
  referenceImageUrl: string;
  width: number;
  height: number;
}

interface State {}

class ImageComparison extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
  }

  render() {
    return (
      <div
        className={styles.imgCompContainer}
        style={{ maxWidth: this.props.width, height: this.props.height }}
      >
        <img
          src={this.props.outputImageUrl}
          className={styles.imageSizeCalculator}
          alt={"left"}
        />
        <ReactCompareImage
          leftImage={this.props.outputImageUrl}
          rightImage={this.props.referenceImageUrl}
        />
      </div>
    );
  }
}

export default ImageComparison;
