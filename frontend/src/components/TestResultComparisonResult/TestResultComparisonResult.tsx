import React from "react";
import { TestResultDto } from "../../catoapimodels";
import styles from "./TestResultComparisonResult.module.scss";
import InfoBox from "../InfoBox/InfoBox";
interface Props {
  testResult: TestResultDto;
}

function TestResultComparisonResult(props: Props) {
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
                    props.testResult.comparison_settings.method
                  ) : (
                    <>&mdash;</>
                  )}
                </td>
              </tr>
              <tr>
                <td>Threshold</td>
                <td data-testid={"comparison-method-threshold"}>
                  {props.testResult.comparison_settings ? (
                    props.testResult.comparison_settings.threshold
                  ) : (
                    <>&mdash;</>
                  )}
                </td>
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
