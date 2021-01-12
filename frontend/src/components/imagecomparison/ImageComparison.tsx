import React, { Component } from "react";
import styles from "./ImageComparison.module.css";
import ReactCompareImage from "react-compare-image";
import { Spinner } from "react-bootstrap";

interface Props {
  outputImageUrl: string;
  referenceImageUrl: string;
  width: number;
  height: number;
  identifier: string;
}

interface State {
  referenceImageLoaded: boolean;
  outputImageLoaded: boolean;
  outputImageUrlToRender: string;
  referenceImageUrlToRender: string;
  isSwapping: boolean;
  heightForRendering: number;
}

class ImageComparison extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      referenceImageLoaded: false,
      outputImageLoaded: false,
      outputImageUrlToRender: props.outputImageUrl,
      referenceImageUrlToRender: props.referenceImageUrl,
      isSwapping: false,
      heightForRendering: 0,
    };
  }

  componentDidUpdate(
    prevProps: Readonly<Props>,
    prevState: Readonly<State>,
    snapshot?: any
  ) {
    let isSwapping =
      this.props.referenceImageUrl !== prevProps.referenceImageUrl ||
      (this.props.outputImageUrl !== prevProps.outputImageUrl &&
        prevProps.identifier === this.props.identifier);

    if (isSwapping) {
      let containerElement = document.getElementById(this.generateId());
      if (containerElement) {
        let height = containerElement.clientHeight;
        this.setState({ heightForRendering: height });
      }
      this.setState({ isSwapping: true });
    }

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
        id={this.generateId()}
        className={styles.imgCompContainer}
        style={
          this.state.isSwapping
            ? {
                maxWidth: this.props.width,
                height: this.state.heightForRendering,
              }
            : { maxWidth: this.props.width }
        }
      >
        <img
          src={this.props.referenceImageUrl}
          className={styles.imageSizeCalculator}
          alt={"left"}
          onLoad={this.checkLoadedReferenceImage}
        />
        <img
          src={this.props.outputImageUrl}
          className={styles.imageSizeCalculator}
          alt={"left"}
          onLoad={this.checkOutputImageLoaded}
        />
        {(this.state.outputImageLoaded && this.state.referenceImageLoaded) ||
        this.state.isSwapping ? (
          <ReactCompareImage
            leftImage={this.state.outputImageUrlToRender}
            rightImage={this.state.referenceImageUrlToRender}
          />
        ) : (
          <div className={styles.spinner}>
            <Spinner animation="border" role="status" variant={"light"}>
              <span className="sr-only">Loading...</span>
            </Spinner>
          </div>
        )}
      </div>
    );
  }
  checkLoadedReferenceImage = () => {
    console.log("loaded");
    this.setState({ referenceImageLoaded: true });
    if (this.state.outputImageLoaded) {
      console.log(this.props.outputImageUrl);
      this.setState({
        outputImageUrlToRender: this.props.outputImageUrl,
        referenceImageUrlToRender: this.props.referenceImageUrl,
        isSwapping: false,
      });
    }
  };
  checkOutputImageLoaded = () => {
    console.log("loaded");
    this.setState({ outputImageLoaded: true });
    if (this.state.referenceImageLoaded) {
      console.log(this.props.outputImageUrl);
      this.setState({
        outputImageUrlToRender: this.props.outputImageUrl,
        referenceImageUrlToRender: this.props.referenceImageUrl,
        isSwapping: false,
      });
    }
  };
  generateId = () => {
    return "ImageComparion" + this.props.identifier;
  };
}

export default ImageComparison;
