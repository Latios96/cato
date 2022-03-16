import React, { useContext, useEffect, useState } from "react";
import axios from "axios";
import Button from "../Button/Button";
import styles from "./UpdateReferenceImageButton.module.scss";
import Spinner from "../Spinner/Spinner";
import InformationIcon from "../InformationIcon/InformationIcon";
import { TestResultUpdateContext } from "../TestResultUpdateContext/TestResultUpdateContext";
import { CanBeEdited } from "../../catoapimodels/catoapimodels";

interface Props {
  testResultId: number;
}

function UpdateReferenceImageButton(props: Props) {
  const [isDoingIo, setIsDoingIo] = useState(false);
  const [isEditable, setIsEditable] = useState<CanBeEdited>({
    can_edit: false,
  });

  const { update } = useContext(TestResultUpdateContext);

  useEffect(() => {
    setIsDoingIo(true);
    axios
      .get(`/api/v1/test_edits/can-edit/${props.testResultId}/reference_image`)
      .then((result) => {
        setIsEditable(result.data);
        setIsDoingIo(false);
      })
      .catch(() => {
        setIsEditable({ can_edit: false });
        setIsDoingIo(false);
      });
  }, [props.testResultId]);

  return (
    <div className={styles.container}>
      <Button
        onClick={() => {
          setIsDoingIo(true);
          axios
            .post("/api/v1/test_edits/reference_image", {
              test_result_id: props.testResultId,
            })
            .then(() => {
              setIsDoingIo(false);
              update(props.testResultId);
            })
            .catch(() => {
              setIsDoingIo(false);
            });
        }}
        disabled={!isEditable.can_edit || isDoingIo}
      >
        Update Reference Image
      </Button>
      {isDoingIo ? (
        <div className={styles.spinner}>
          <Spinner />
        </div>
      ) : !isEditable.can_edit ? (
        <div className={styles.information}>
          <InformationIcon informationText={isEditable.message || ""} />
        </div>
      ) : (
        <></>
      )}
    </div>
  );
}

export default UpdateReferenceImageButton;
