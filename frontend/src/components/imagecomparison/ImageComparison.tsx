import React, { Component } from "react";
import styles from "./ImageComparison.module.css";
import ReactCompareImage from "react-compare-image";

interface Props {
  outputImageUrl: string;
  referenceImageUrl: string;
}

interface State {
  imgWidth: number;
  imgHeight: number;
}

class ImageComparison extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { imgHeight: 0, imgWidth: 0 };
  }

  render() {
    return (
      <div
        className={styles.imgCompContainer}
        style={{ maxWidth: this.state.imgWidth }}
      >
        <img
          src={this.props.outputImageUrl}
          className={styles.imageSizeCalculator}
          onLoad={(e) => {
            console.log(e.currentTarget.clientHeight);
            this.setState({
              imgHeight: e.currentTarget.naturalHeight,
              imgWidth: e.currentTarget.naturalWidth,
            });
          }}
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
