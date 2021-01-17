import React from "react";
import Modal from "react-modal";
interface Props {
  modalIsOpen: boolean;
}
const ImageComparisonFullscreenModal = (props: Props) => {
  return <Modal isOpen={props.modalIsOpen} />;
};

export default ImageComparisonFullscreenModal;
