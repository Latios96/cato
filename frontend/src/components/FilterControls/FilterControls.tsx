import React from "react";
import { Form } from "react-bootstrap";
import styles from "./FilterControls.module.scss";
import { FilterOptions } from "../../models/FilterOptions";
import { getNiceName } from "../../models/testFailureReasonNiceNames";
import {
  StatusFilter,
  TestFailureReason,
} from "../../catoapimodels/catoapimodels";

interface Props {
  currentFilterOptions: FilterOptions;
  filterOptionsChanged: (filterOptions: FilterOptions) => void;
  failureReasonIsNotFilterable?: boolean;
}

function FilterControls(props: Props) {
  return (
    <div className={styles.filterControlContainer}>
      <div className={styles.checkboxContainer}>
        <Form.Check
          inline
          id="All"
          label="All"
          name={"Filter"}
          type={"radio"}
          checked={props.currentFilterOptions.status === StatusFilter.NONE}
          onClick={() =>
            props.filterOptionsChanged(
              props.currentFilterOptions
                .withChangedStatusFilter(StatusFilter.NONE)
                .withChangedFailureReason(undefined)
            )
          }
          onChange={(e) => {}}
        />
        <Form.Check
          inline
          id="Failed"
          label="Failed"
          name={"Filter"}
          type={"radio"}
          checked={props.currentFilterOptions.status === StatusFilter.FAILED}
          onClick={() =>
            props.filterOptionsChanged(
              props.currentFilterOptions.withChangedStatusFilter(
                StatusFilter.FAILED
              )
            )
          }
          onChange={(e) => {}}
        />
        <Form.Check
          inline
          id="Success"
          label="Success"
          name={"Filter"}
          type={"radio"}
          checked={props.currentFilterOptions.status === StatusFilter.SUCCESS}
          onClick={() =>
            props.filterOptionsChanged(
              props.currentFilterOptions
                .withChangedStatusFilter(StatusFilter.SUCCESS)
                .withChangedFailureReason(undefined)
            )
          }
          onChange={(e) => {}}
        />
        <Form.Check
          inline
          id="Running"
          label="Running"
          name={"Filter"}
          type={"radio"}
          checked={props.currentFilterOptions.status === StatusFilter.RUNNING}
          onClick={() =>
            props.filterOptionsChanged(
              props.currentFilterOptions
                .withChangedStatusFilter(StatusFilter.RUNNING)
                .withChangedFailureReason(undefined)
            )
          }
          onChange={(e) => {}}
        />
        <Form.Check
          inline
          id="Not Started"
          label={"Not Started"}
          name={"Filter"}
          type={"radio"}
          checked={
            props.currentFilterOptions.status === StatusFilter.NOT_STARTED
          }
          onClick={() =>
            props.filterOptionsChanged(
              props.currentFilterOptions
                .withChangedStatusFilter(StatusFilter.NOT_STARTED)
                .withChangedFailureReason(undefined)
            )
          }
          onChange={(e) => {}}
        />
      </div>
      {!props.failureReasonIsNotFilterable &&
      props.currentFilterOptions.status === StatusFilter.FAILED ? (
        <div className={styles.failureReasonFilterControls}>
          <Form.Label htmlFor={"failureReasonSelect"}>
            Failure Reason
          </Form.Label>
          <Form.Control
            id={"failureReasonSelect"}
            as="select"
            onChange={(event) => {
              const newValue =
                event.currentTarget.value !== "NONE"
                  ? TestFailureReason[
                      event.currentTarget
                        .value as keyof typeof TestFailureReason
                    ]
                  : undefined;
              props.filterOptionsChanged(
                props.currentFilterOptions.withChangedFailureReason(newValue)
              );
            }}
            value={
              props.currentFilterOptions.failureReason
                ? props.currentFilterOptions.failureReason
                : "NONE"
            }
          >
            {" "}
            <option value={"NONE"}>None</option>
            {Object.keys(TestFailureReason).map((reason) => {
              return (
                <option key={reason} value={reason}>
                  {getNiceName(
                    TestFailureReason[reason as keyof typeof TestFailureReason]
                  )}
                </option>
              );
            })}
          </Form.Control>
        </div>
      ) : (
        <></>
      )}
    </div>
  );
}

export default FilterControls;
