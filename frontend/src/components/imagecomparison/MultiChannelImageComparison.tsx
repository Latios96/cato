import React, { Component } from "react";
import CatoImage from "../../models/CatoImage";
import ImageComparison from "./ImageComparison";
import { ImageDto } from "../../catoapimodels";

interface Props {
  imageOutput: ImageDto;
  referenceImage: ImageDto;
}

interface State {
  imageOutputHasLoaded: boolean;
  selectedChannel: string;
  width: number;
  height: number;
}

class MultiChannelImageComparison extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      imageOutputHasLoaded: false,
      selectedChannel: "rgb",
      width: 0,
      height: 0,
    };
  }

  componentDidMount() {}

  render() {
    return (
      <div style={this.state.height ? { height: this.state.height } : {}}>
        {this.props.imageOutput && this.props.referenceImage ? (
          this.renderImageComparison(
            this.props.imageOutput,
            this.props.referenceImage
          )
        ) : (
          <React.Fragment />
        )}
      </div>
    );
  }

  renderImageComparison = (imageOutput: ImageDto, referenceImage: ImageDto) => {
    return (
      <React.Fragment>
        <select onChange={this.handleChange}>
          {imageOutput.channels.map((channel) => {
            return (
              <option key={channel.id} value={channel.name}>
                {channel.name}
              </option>
            );
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
          sizeIsKnownCallback={(width, height) => {
            this.setState({ width: width, height: height });
          }}
        />
      </React.Fragment>
    );
  };

  channelFileIdByName = (image: ImageDto, name: string) => {
    let channel = this.channelByName(image, name);
    if (channel === null) {
      return null;
    }
    return channel.fileId;
  };

  channelByName = (image: ImageDto, name: string) => {
    let index = image.channels.findIndex((ch) => {
      return ch.name === name;
    });
    if (index === -1) {
      return null;
    }
    return image.channels[index];
  };

  handleChange = (event: React.FormEvent<HTMLSelectElement>) => {
    let selectedChannel = event.currentTarget.value;
    this.setState({ selectedChannel: selectedChannel });
  };
}

export default MultiChannelImageComparison;
