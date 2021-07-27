import React, { Component } from "react";
import SingleChannelComparison from "../SingleChannelComparison/SingleChannelComparison";
import { ImageDto } from "../../../catoapimodels";
import { Form } from "react-bootstrap";
import styles from "./MultiChannelImageComparion.module.scss";
import { CompareModes } from "../CompareModes";
import AlphaButton from "../AlphaButton/AlphaButton";

interface Props {
  imageOutput: ImageDto | null | undefined;
  referenceImage: ImageDto | null | undefined;
  diffImage: ImageDto | null | undefined;
  id: string;
}

interface State {
  imageOutputHasLoaded: boolean;
  selectedChannel: string;
  width: number;
  height: number;
  selectedMode: CompareModes;
  channelBeforeAlpha: string;
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
      channelBeforeAlpha: "rgb",
    };
  }

  componentDidMount() {}

  render() {
    return (
      <div style={this.state.height ? { height: this.state.height } : {}}>
        {this.props.imageOutput && this.props.referenceImage ? (
          this.renderImageComparison(
            this.props.imageOutput,
            this.props.referenceImage,
            this.props.diffImage
          )
        ) : (
          <React.Fragment />
        )}
      </div>
    );
  }

  renderImageComparison = (
    imageOutput: ImageDto | null | undefined,
    referenceImage: ImageDto | null | undefined,
    diffImage: ImageDto | null | undefined
  ) => {
    const imageOutputOrReferenceImage = this.getDefined(
      imageOutput,
      referenceImage
    );
    return (
      <React.Fragment>
        <form>
          <Form.Control
            className={styles.selectChannel}
            as="select"
            custom
            onChange={this.handleChange}
            value={this.state.selectedChannel}
          >
            {(imageOutputOrReferenceImage
              ? imageOutputOrReferenceImage.channels
              : []
            ).map((channel) => {
              return (
                <option key={channel.id} value={channel.name}>
                  {channel.name}
                </option>
              );
            })}
          </Form.Control>

          <AlphaButton
            isToggled={this.state.selectedChannel === "alpha"}
            onClick={() => this.toggleAlpha()}
            clickable={this.hasAlpha()}
          />

          <Form.Check
            id={"selected-swipe-mode-swipe" + this.props.id}
            inline
            label="Swipe"
            name={"CompareMode"}
            type={"radio"}
            checked={this.state.selectedMode === CompareModes.SWIPE}
            onChange={() => this.setState({ selectedMode: CompareModes.SWIPE })}
          />
          <Form.Check
            id={"selected-swipe-mode-diff" + this.props.id}
            inline
            label="Diff"
            name={"CompareMode"}
            type={"radio"}
            checked={this.state.selectedMode === CompareModes.DIFF}
            onChange={() => this.setState({ selectedMode: CompareModes.DIFF })}
            disabled={!this.props.diffImage}
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
          diffImageUrl={
            "/api/v1/files/" + this.channelFileIdByName(diffImage, "rgb")
          }
          width={
            imageOutputOrReferenceImage ? imageOutputOrReferenceImage.width : 0
          }
          height={
            imageOutputOrReferenceImage ? imageOutputOrReferenceImage.height : 0
          }
          identifier={"test"}
          mode={this.state.selectedMode}
        />
      </React.Fragment>
    );
  };

  channelFileIdByName = (image: ImageDto | null | undefined, name: string) => {
    if (!image) {
      return "0";
    }
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

  toggleAlpha = () => {
    if (!this.hasAlpha()) {
      return;
    }
    const isAlpha = this.state.selectedChannel === "alpha";
    if (isAlpha) {
      this.setState({
        channelBeforeAlpha: this.state.selectedChannel,
        selectedChannel: this.state.channelBeforeAlpha,
      });
      return;
    }
    this.setState({
      channelBeforeAlpha: this.state.selectedChannel,
      selectedChannel: "alpha",
    });
  };

  hasAlpha = () => {
    if (!this.props.referenceImage) {
      return false;
    }
    return this.channelByName(this.props.referenceImage, "alpha") !== null;
  };

  getDefined = (
    first: ImageDto | null | undefined,
    second: ImageDto | null | undefined
  ) => {
    return first ? first : second;
  };
}

export default MultiChannelImageComparison;
