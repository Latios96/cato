import React from "react";
import Modal from "react-modal";
import { X } from "react-bootstrap-icons";
import { Button } from "react-bootstrap";
import { ImageDto } from "../../../catoapimodels";
import MultiChannelImageComparison from "../MultiChannelImageComparison/MultiChannelImageComparison";
import styles from "./ImageComparisonFullScreenModal.module.scss";

interface Props {
  modalIsOpen: boolean;
  onCloseRequest: () => void;
  imageOutput: ImageDto;
  referenceImage: ImageDto;
}

const ImageComparisonFullScreenModal = (props: Props) => {
  return (
    <Modal
      id="app-image-comparison-modal"
      isOpen={props.modalIsOpen}
      className={styles.modal}
      overlayClassName={styles.modalOverlay}
      onRequestClose={props.onCloseRequest}
    >
      <div className={styles.closeButtonContainer}>
        <Button
          id="app-close-image-comparison-modal"
          onClick={props.onCloseRequest}
          variant={"link"}
          className={styles.buttonNoShadowOnFocus}
        >
          <X size={22} />
        </Button>
      </div>
      <MultiChannelImageComparison
        id={"modal"}
        imageOutput={props.imageOutput}
        referenceImage={props.referenceImage}
      />
    </Modal>
  );
};

export default ImageComparisonFullScreenModal;
