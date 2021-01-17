import React from "react";
import Modal from "react-modal";
import { X } from "react-bootstrap-icons";
import { Button } from "react-bootstrap";
import { ImageDto } from "../../catoapimodels";
import MultiChannelImageComparison from "./MultiChannelImageComparison";
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
      isOpen={props.modalIsOpen}
      className={styles.modal}
      overlayClassName={styles.modalOverlay}
      onRequestClose={props.onCloseRequest}
    >
      <div className={styles.closeButtonContainer}>
        <Button onClick={props.onCloseRequest}>
          <X size={22} />
        </Button>
      </div>
      <MultiChannelImageComparison
        imageOutput={props.imageOutput}
        referenceImage={props.referenceImage}
      />
    </Modal>
  );
};

export default ImageComparisonFullScreenModal;
