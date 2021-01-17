import React, { useState } from "react";
import { ImageDto } from "../../catoapimodels";
import MultiChannelImageComparison from "./MultiChannelImageComparison";
import { Button } from "react-bootstrap";
import { Fullscreen } from "react-bootstrap-icons";
import ImageComparisonFullscreenModal from "./ImageComparisonFullscreenModal";
interface Props {
  imageOutput: ImageDto;
  referenceImage: ImageDto;
}
const ImageComparison = (props: Props) => {
  const [modalIsOpen, setModalOpen] = useState(false);
  return (
    <div>
      <MultiChannelImageComparison
        imageOutput={props.imageOutput}
        referenceImage={props.referenceImage}
      />
      <Button onClick={() => setModalOpen(true)}>
        <Fullscreen />
      </Button>
      <ImageComparisonFullscreenModal modalIsOpen={modalIsOpen} />
    </div>
  );
};

export default ImageComparison;
