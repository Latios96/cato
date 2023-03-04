import React, { Component } from "react";
import styles from "./SingleChannelComparison.module.css";
import ReactCompareImage from "react-compare-image";
import { Spinner } from "react-bootstrap";
import { CompareModes } from "../CompareModes";
import DiffImageDisplay from "../DiffImageDisplay/DiffImageDisplay";
import { ComparisonMethod } from "../../../catoapimodels/catoapimodels";

interface Props {
  outputImageUrl: string;
  referenceImageUrl: string;
  diffImageUrl: string;
  width: number;
  height: number;
  identifier: string;
  mode: CompareModes;
  comparisonMethod: ComparisonMethod;
}

interface State {
  referenceImageLoaded: boolean;
  outputImageLoaded: boolean;
  outputImageUrlToRender: string;
  referenceImageUrlToRender: string;
  isSwapping: boolean;
  heightForRendering: number;
}

class SingleChannelComparison extends Component<Props, State> {
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
  componentDidMount() {
    this.updateHeight();
  }

  private updateHeight() {
    let containerElement = document.getElementById(this.generateId());
    if (containerElement) {
      let width = containerElement.clientWidth;
      let aspectRatio = this.props.height / this.props.width;
      let initialHeight = width * aspectRatio;
      this.setState({ heightForRendering: initialHeight });
    }
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
      this.updateHeight();
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
      <div>
        <div
          id={this.generateId()}
          className={styles.imgCompContainer}
          style={
            this.state.heightForRendering
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
            this.props.mode === CompareModes.SWIPE ? (
              <ReactCompareImage
                leftImage={this.state.referenceImageUrlToRender}
                rightImage={this.state.outputImageUrlToRender}
                key={this.state.outputImageUrlToRender}
              />
            ) : (
              <DiffImageDisplay
                imageUrl={this.props.diffImageUrl}
                comparisonMethod={this.props.comparisonMethod}
              />
            )
          ) : (
            <div className={styles.spinner}>
              <Spinner animation="border" role="status" variant={"light"}>
                <span className="sr-only">Loading...</span>
              </Spinner>
            </div>
          )}
          {this.props.mode === CompareModes.SWIPE ? (
            <>
              <span className={styles.referenceText}>Reference</span>
              <span className={styles.outputText}>Output</span>
            </>
          ) : (
            ""
          )}
        </div>
      </div>
    );
  }
  checkLoadedReferenceImage = () => {
    this.setState({ referenceImageLoaded: true });
    if (this.state.outputImageLoaded) {
      this.setState({
        outputImageUrlToRender: this.props.outputImageUrl,
        referenceImageUrlToRender: this.props.referenceImageUrl,
        isSwapping: false,
      });
    }
  };
  checkOutputImageLoaded = () => {
    this.setState({ outputImageLoaded: true });
    if (this.state.referenceImageLoaded) {
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

export default SingleChannelComparison;
