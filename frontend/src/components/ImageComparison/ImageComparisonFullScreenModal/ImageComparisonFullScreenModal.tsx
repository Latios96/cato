import React from "react";
import Modal from "react-modal";
import { X } from "react-bootstrap-icons";
import { Button } from "react-bootstrap";
import MultiChannelImageComparison from "../MultiChannelImageComparison/MultiChannelImageComparison";
import styles from "./ImageComparisonFullScreenModal.module.scss";
import { ComparisonMethod, Image } from "../../../catoapimodels/catoapimodels";

interface Props {
  modalIsOpen: boolean;
  onCloseRequest: () => void;
  imageOutput: Image | null | undefined;
  referenceImage: Image | null | undefined;
  diffImage: Image | null | undefined;
  comparisonMethod: ComparisonMethod;
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
        diffImage={props.diffImage}
        comparisonMethod={props.comparisonMethod}
      />
    </Modal>
  );
};

export default ImageComparisonFullScreenModal;
