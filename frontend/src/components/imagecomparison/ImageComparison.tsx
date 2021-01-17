import React, { useState } from "react";
import { ImageDto } from "../../catoapimodels";
import MultiChannelImageComparison from "./MultiChannelImageComparison";
import { Button } from "react-bootstrap";
import { Fullscreen } from "react-bootstrap-icons";
import ImageComparisonFullScreenModal from "./ImageComparisonFullScreenModal";
import styles from "./ImageComparison.module.scss";
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

      <div className={styles.fullscreenButtonContainer}>
        <Button onClick={() => setModalOpen(true)}>
          <Fullscreen />
        </Button>
      </div>

      <ImageComparisonFullScreenModal
        modalIsOpen={modalIsOpen}
        onCloseRequest={() => setModalOpen(false)}
        imageOutput={props.imageOutput}
        referenceImage={props.referenceImage}
      />
    </div>
  );
};

export default ImageComparison;
