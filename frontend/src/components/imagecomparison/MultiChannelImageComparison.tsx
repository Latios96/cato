import React, { ChangeEvent, Component } from "react";
import ImageComparison from "./ImageComparison";
import { ImageDto } from "../../catoapimodels";
import { Form } from "react-bootstrap";
import styles from "./MultiChannelImageComparion.module.scss";

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
        <Form.Control
          className={styles.selectChannel}
          as="select"
          custom
          onChange={this.handleChange}
        >
          {imageOutput.channels.map((channel) => {
            return (
              <option key={channel.id} value={channel.name}>
                {channel.name}
              </option>
            );
          })}
        </Form.Control>
        <ImageComparison
          outputImageUrl={
            "/api/v1/files/" +
            this.channelFileIdByName(imageOutput, this.state.selectedChannel)
          }
          referenceImageUrl={
            "/api/v1/files/" +
            this.channelFileIdByName(referenceImage, this.state.selectedChannel)
          }
          width={imageOutput.width}
          height={imageOutput.height}
          identifier={"test"}
        />
      </React.Fragment>
    );
  };

  channelFileIdByName = (image: ImageDto, name: string) => {
    let channel = this.channelByName(image, name);
    if (channel === null) {
      return null;
    }
    return channel.file_id;
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

  handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    let selectedChannel = event.currentTarget.value;
    this.setState({ selectedChannel: selectedChannel });
  };
}

export default MultiChannelImageComparison;
