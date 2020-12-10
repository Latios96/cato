import React, { Component } from "react";
import styles from "./ImageComparison.module.css";

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
        style={
          this.state.imgHeight !== 0 ? { height: this.state.imgHeight } : {}
        }
      >
        <img
          onLoad={(e) => {
            console.log(e.currentTarget.clientHeight);
            this.setState({
              imgHeight: e.currentTarget.naturalHeight,
              imgWidth: e.currentTarget.naturalWidth,
            });
          }}
          src={this.props.outputImageUrl}
          className={styles.imgCompImg}
        />
        <img src={this.props.referenceImageUrl} className={styles.imgCompImg} />
      </div>
    );
  }
}

export default ImageComparison;
