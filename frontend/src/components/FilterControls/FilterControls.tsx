import React from "react";
import { Form } from "react-bootstrap";
import styles from "./FilterControls.module.scss";
import { FilterOptions, StatusFilter } from "../../models/FilterOptions";

interface Props {
  currentFilterOptions: FilterOptions;
  filterOptionsChanged: (filterOptions: FilterOptions) => void;
}

function FilterControls(props: Props) {
  return (
    <div className={styles.filterControlContainer}>
      <Form.Check
        inline
        id="All"
        label="All"
        name={"Filter"}
        type={"radio"}
        checked={props.currentFilterOptions.status === StatusFilter.NONE}
        onClick={() =>
          props.filterOptionsChanged(
            props.currentFilterOptions.withChangedStatusFilter(
              StatusFilter.NONE
            )
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
            props.currentFilterOptions.withChangedStatusFilter(
              StatusFilter.SUCCESS
            )
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
            props.currentFilterOptions.withChangedStatusFilter(
              StatusFilter.RUNNING
            )
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
        checked={props.currentFilterOptions.status === StatusFilter.NOT_STARTED}
        onClick={() =>
          props.filterOptionsChanged(
            props.currentFilterOptions.withChangedStatusFilter(
              StatusFilter.NOT_STARTED
            )
          )
        }
        onChange={(e) => {}}
      />
    </div>
  );
}

export default FilterControls;
