import React, { Component, SyntheticEvent } from "react";
import Image from "../../models/Image";
import ImageChannel from "../../models/ImageChannel";
import ImageComparison from "./ImageComparison";

interface Props {
  imageOutputId: number;
  referenceImageId: number;
}

interface State {
  imageOutputHasLoaded: boolean;
  imageOutput: Image | null;
  referenceImage: Image | null;
  selectedChannel: string;
}

class MultiChannelImageComparison extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      imageOutputHasLoaded: false,
      imageOutput: null,
      referenceImage: null,
      selectedChannel: "rgb",
    };
  }

  componentDidMount() {
    fetch("/api/v1/images/" + this.props.imageOutputId)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ imageOutput: result });
        },
        (error) => {
          console.log(error);
        }
      );
    fetch("/api/v1/images/" + this.props.referenceImageId)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ referenceImage: result });
        },
        (error) => {
          console.log(error);
        }
      );
  }

  render() {
    return (
      <div>
        {this.state.imageOutput && this.state.referenceImage ? (
          this.renderImageComparison(
            this.state.imageOutput,
            this.state.referenceImage
          )
        ) : (
          <React.Fragment />
        )}
      </div>
    );
  }

  renderImageComparison = (imageOutput: Image, referenceImage: Image) => {
    return (
      <React.Fragment>
        <select onChange={this.handleChange}>
          {imageOutput.channels.map((channel) => {
            return <option value={channel.name}>{channel.name}</option>;
          })}
        </select>
        <ImageComparison
          outputImageUrl={
            "/api/v1/files/" +
            this.channelFileIdByName(imageOutput, this.state.selectedChannel)
          }
          referenceImageUrl={
            "/api/v1/files/" +
            this.channelFileIdByName(referenceImage, this.state.selectedChannel)
          }
        />
      </React.Fragment>
    );
  };

  channelFileIdByName = (image: Image, name: string) => {
    let channel = this.channelByName(image, name);
    if (channel === null) {
      return null;
    }
    return channel.file_id;
  };

  channelByName = (image: Image, name: string) => {
    let index = image.channels.findIndex((ch) => {
      return ch.name === name;
    });
    if (index === -1) {
      return null;
    }
    return image.channels[index];
  };

  handleChange = (event: React.FormEvent<HTMLSelectElement>) => {
    this.setState({ selectedChannel: event.currentTarget.value });
  };
}

export default MultiChannelImageComparison;
