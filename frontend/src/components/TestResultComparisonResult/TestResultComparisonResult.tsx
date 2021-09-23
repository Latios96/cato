import React, { useEffect, useState } from "react";
import {
  ComparisonMethodDto,
  ComparisonSettingsDto,
  TestResultDto,
} from "../../catoapimodels";
import styles from "./TestResultComparisonResult.module.scss";
import InfoBox from "../InfoBox/InfoBox";
import { Form } from "react-bootstrap";
import axios from "axios";
import Spinner from "../Spinner/Spinner";

interface Props {
  testResult: TestResultDto;
}
const getInitialComparisonSettings = (
  comparisonSettings?: ComparisonSettingsDto | null
) =>
  comparisonSettings
    ? comparisonSettings
    : {
        method: ComparisonMethodDto.SSIM,
        threshold: 0.8,
      };
function TestResultComparisonResult(props: Props) {
  const [isEditing, setEditing] = useState(false);
  const [isUpdating, setUpdating] = useState(false);

  const [currentComparisonSettings, setCurrentComparisonSettings] =
    useState<ComparisonSettingsDto>(
      getInitialComparisonSettings(props.testResult.comparison_settings)
    );

  useEffect(() => {
    setCurrentComparisonSettings(
      getInitialComparisonSettings(props.testResult.comparison_settings)
    );
  }, [props.testResult]);

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
                        value={currentComparisonSettings.method}
                        data-testid={"edit-comparison-settings-method"}
                      >
                        {Object.values(ComparisonMethodDto).map((v) => {
                          return <option key={v}>{v}</option>;
                        })}
                      </Form.Control>
                    ) : (
                      currentComparisonSettings.method
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
                          value={currentComparisonSettings.threshold}
                          onChange={(v) =>
                            setCurrentComparisonSettings({
                              ...currentComparisonSettings,
                              threshold: parseFloat(v.target.value),
                            })
                          }
                        />
                        <button
                          className={styles.button}
                          onClick={() => {
                            setCurrentComparisonSettings({
                              ...currentComparisonSettings,
                              threshold: props.testResult.error_value || 0.8,
                            });
                          }}
                        >
                          match error
                        </button>
                      </>
                    ) : (
                      currentComparisonSettings.threshold
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
                            new_value: currentComparisonSettings,
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

export default TestResultComparisonResult;
