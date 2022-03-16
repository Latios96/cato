import React from "react";
import styles from "./TestResultComparisonResult.module.scss";
import InfoBox from "../InfoBox/InfoBox";
import { Form } from "react-bootstrap";
import Spinner from "../Spinner/Spinner";
import InformationIcon from "../InformationIcon/InformationIcon";
import { Action, ActionType, State } from "./reducer";
import Button from "../Button/Button";
import {
  ComparisonMethod,
  ComparisonSettings,
  TestResultDto,
} from "../../catoapimodels/catoapimodels";

export type TestResultDtoComparisonPick = Pick<
  TestResultDto,
  "comparison_settings" | "error_value"
>;

interface Props {
  testResult: TestResultDtoComparisonPick;
  state: State;
  dispatch: (action: Action) => void;
  updateComparisonSettings: (settings: ComparisonSettings) => void;
}

export function TestResultComparisonResultImpl(props: Props) {
  const state = props.state;

  const update = () =>
    props.updateComparisonSettings({
      method:
        state.currentMethod === ComparisonMethod.SSIM
          ? ComparisonMethod.SSIM
          : ComparisonMethod.SSIM,
      threshold: parseFloat(state.currentThreshold),
    });

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
                    state.isEditing ? (
                      <Form.Control
                        as="select"
                        size={"sm"}
                        className={styles.methodInput}
                        value={state.currentMethod}
                        data-testid={"edit-comparison-settings-method"}
                      >
                        {Object.values(ComparisonMethod).map((v) => {
                          return <option key={v}>{v}</option>;
                        })}
                      </Form.Control>
                    ) : (
                      state.currentMethod
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
                    state.isEditing ? (
                      <>
                        <input
                          data-testid={"edit-comparison-settings-threshold"}
                          type="number"
                          step="0.01"
                          className={styles.thresholdInput}
                          value={state.currentThreshold}
                          onChange={(v) =>
                            props.dispatch({
                              type: ActionType.SET_CURRENT_THRESHOLD,
                              payload: v.target.value,
                            })
                          }
                          onKeyDown={(event) => {
                            if (event.key === "Enter") {
                              update();
                            }
                          }}
                        />
                        <Button
                          onClick={() => {
                            props.dispatch({
                              type: ActionType.SET_CURRENT_THRESHOLD,
                              payload: toFixed(props.testResult.error_value),
                            });
                          }}
                          solid={true}
                        >
                          match error
                        </Button>
                      </>
                    ) : (
                      state.currentThreshold
                    )
                  ) : (
                    <>&mdash;</>
                  )}
                </td>
              </tr>
              <tr className={styles.buttonRow}>
                {state.isEditing ? (
                  <>
                    <Button onClick={update} primary={true} solid={true}>
                      OK
                    </Button>
                    <Button
                      onClick={() =>
                        props.dispatch({
                          type: ActionType.CANCEL,
                        })
                      }
                      solid={true}
                    >
                      Cancel
                    </Button>
                  </>
                ) : (
                  <>
                    <Button
                      onClick={() =>
                        props.dispatch({
                          type: ActionType.START_EDITING,
                        })
                      }
                      disabled={
                        state.isEditableChecking || !state.isEditable.can_edit
                      }
                      solid={true}
                    >
                      Edit
                    </Button>
                    {state.isUpdating || state.isEditableChecking ? (
                      <div className={styles.spinner}>
                        <Spinner />
                      </div>
                    ) : !state.isEditable.can_edit ? (
                      <div className={styles.information}>
                        <InformationIcon
                          informationText={state.isEditable.message || ""}
                        />
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
                  {props.testResult.error_value ? (
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
function toFixed(error_value?: number | "NaN" | null) {
  if (error_value === "NaN" || !error_value) {
    return "0.8";
  }
  return error_value.toFixed(3);
}
