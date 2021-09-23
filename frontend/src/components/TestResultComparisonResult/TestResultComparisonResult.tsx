import React, { useEffect, useState } from "react";
import { ComparisonMethodDto, TestResultDto } from "../../catoapimodels";
import styles from "./TestResultComparisonResult.module.scss";
import InfoBox from "../InfoBox/InfoBox";
import { Form } from "react-bootstrap";
import axios from "axios";
import Spinner from "../Spinner/Spinner";

interface Props {
  testResult: TestResultDto;
}

function TestResultComparisonResult(props: Props) {
  const [isEditing, setEditing] = useState(false);
  const [isUpdating, setUpdating] = useState(false);

  const [currentThreshold, setCurrentThreshold] = useState<string>(
    getInitialThreshold(props)
  );
  const [currentMethod, setCurrentMethod] = useState<ComparisonMethodDto>(
    getInitialMethod(props)
  );

  useEffect(() => {
    setCurrentMethod(getInitialMethod(props));
    setCurrentThreshold(getInitialThreshold(props));
  }, [props, props.testResult]);

  return (
    <InfoBox className={styles.infoBox}>
      <div className={styles.testResultComparisonResult}>
        <div>
          <table>
            <tbody>
              <tr>
                <td>Comparison Method</td>
                <td data-testid={"comparison-method-method"}>
                  {props.testResult.comparison_settings ? (
                    isEditing ? (
                      <Form.Control
                        as="select"
                        size={"sm"}
                        className={styles.methodInput}
                        value={currentMethod}
                        data-testid={"edit-comparison-settings-method"}
                      >
                        {Object.values(ComparisonMethodDto).map((v) => {
                          return <option key={v}>{v}</option>;
                        })}
                      </Form.Control>
                    ) : (
                      currentMethod
                    )
                  ) : (
                    <>&mdash;</>
                  )}
                </td>
              </tr>
              <tr>
                <td>Threshold</td>
                <td data-testid={"comparison-method-threshold"}>
                  {props.testResult.comparison_settings ? (
                    isEditing ? (
                      <>
                        <input
                          data-testid={"edit-comparison-settings-threshold"}
                          type="number"
                          step="0.01"
                          className={styles.thresholdInput}
                          value={currentThreshold}
                          onChange={(v) => setCurrentThreshold(v.target.value)}
                        />
                        <button
                          className={styles.button}
                          onClick={() => {
                            setCurrentThreshold(
                              toFixed(props.testResult.error_value)
                            );
                          }}
                        >
                          match error
                        </button>
                      </>
                    ) : (
                      currentThreshold
                    )
                  ) : (
                    <>&mdash;</>
                  )}
                </td>
              </tr>
              <tr>
                {isEditing ? (
                  <>
                    <button
                      className={styles.button}
                      onClick={() => {
                        setEditing(false);
                        setUpdating(true);
                        axios
                          .post("/api/v1/test_edits/comparison_settings", {
                            test_result_id: props.testResult.id,
                            new_value: {
                              method: currentMethod,
                              threshold: parseFloat(currentThreshold),
                            },
                          })
                          .then(() => {
                            setUpdating(false);
                          });
                      }}
                      data-primary={true}
                    >
                      OK
                    </button>
                    <button
                      className={styles.button}
                      onClick={() => setEditing(false)}
                    >
                      Cancel
                    </button>
                  </>
                ) : (
                  <>
                    <button
                      className={styles.button}
                      onClick={() => setEditing(true)}
                      disabled={!props.testResult.comparison_settings}
                    >
                      Edit
                    </button>

                    {isUpdating ? (
                      <div className={styles.updatingSpinner}>
                        <Spinner />
                      </div>
                    ) : (
                      <></>
                    )}
                  </>
                )}
              </tr>
            </tbody>
          </table>
        </div>
        <div>
          <table>
            <tbody>
              <tr>
                <td>Error value</td>
                <td data-testid={"error-value"}>
                  {props.testResult.error_value &&
                  props.testResult.error_value !== "NaN" ? (
                    props.testResult.error_value.toFixed(3)
                  ) : (
                    <>&mdash;</>
                  )}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </InfoBox>
  );
}
function getInitialThreshold(props: Props) {
  if (
    props.testResult.comparison_settings &&
    props.testResult.comparison_settings.threshold !== "NaN"
  ) {
    return props.testResult.comparison_settings.threshold.toFixed(3);
  }
  return "0.8";
}

function getInitialMethod(props: Props) {
  return (
    props.testResult.comparison_settings?.method || ComparisonMethodDto.SSIM
  );
}
function toFixed(error_value?: number | "NaN" | null) {
  if (error_value === "NaN" || !error_value) {
    return "0.8";
  }
  return error_value.toFixed(3);
}
export default TestResultComparisonResult;
