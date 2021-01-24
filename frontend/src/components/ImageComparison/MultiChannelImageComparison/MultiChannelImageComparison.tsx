import React, { Component } from "react";
import SingleChannelComparison from "../SingleChannelComparison/SingleChannelComparison";
import { ImageDto } from "../../../catoapimodels";
import { Form } from "react-bootstrap";
import styles from "./MultiChannelImageComparion.module.scss";
import { CompareModes } from "../CompareModes";

interface Props {
  imageOutput: ImageDto;
  referenceImage: ImageDto;
  id: string;
}

interface State {
  imageOutputHasLoaded: boolean;
  selectedChannel: string;
  width: number;
  height: number;
  selectedMode: CompareModes;
}

class MultiChannelImageComparison extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      imageOutputHasLoaded: false,
      selectedChannel: "rgb",
      width: 0,
      height: 0,
      selectedMode: CompareModes.SWIPE,
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
        <form>
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

          <Form.Check
            id={"selected-swipe-mode-swipe" + this.props.id}
            inline
            label="Swipe"
            name={"CompareMode"}
            type={"radio"}
            checked={this.state.selectedMode === CompareModes.SWIPE}
            onChange={() => this.setState({ selectedMode: CompareModes.SWIPE })}
            onClick={(e) => console.log("clicjed")}
          />
          <Form.Check
            id={"selected-swipe-mode-diff" + this.props.id}
            inline
            label="Diff"
            name={"CompareMode"}
            type={"radio"}
            checked={this.state.selectedMode === CompareModes.DIFF}
            onChange={() => this.setState({ selectedMode: CompareModes.DIFF })}
          />
        </form>
        <SingleChannelComparison
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
          mode={this.state.selectedMode}
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