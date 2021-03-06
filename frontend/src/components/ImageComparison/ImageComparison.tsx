import React, { useState } from "react";
import { ImageDto } from "../../catoapimodels";
import MultiChannelImageComparison from "./MultiChannelImageComparison/MultiChannelImageComparison";
import { Button } from "react-bootstrap";
import { Fullscreen } from "react-bootstrap-icons";
import ImageComparisonFullScreenModal from "./ImageComparisonFullScreenModal/ImageComparisonFullScreenModal";
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
        id={"default-compare"}
        imageOutput={props.imageOutput}
        referenceImage={props.referenceImage}
      />

      <div className={styles.fullscreenButtonContainer}>
        <Button
          id="app-open-image-comparison-modal"
          onClick={(e) => {
            e.preventDefault();
            setModalOpen(true);
          }}
          className={styles.buttonNoShadowOnFocus}
          variant={"link"}
        >
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
