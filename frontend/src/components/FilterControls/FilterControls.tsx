import React from "react";
import { Form } from "react-bootstrap";
import styles from "./FilterControls.module.scss";
import { StatusFilter, FilterOptions } from "../../models/FilterOptions";
interface Props {
  currentFilterOptions: FilterOptions;
  statusFilterChanged: (filter: StatusFilter) => void;
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
        onClick={() => props.statusFilterChanged(StatusFilter.NONE)}
        onChange={(e) => {}}
      />
      <Form.Check
        inline
        id="Failed"
        label="Failed"
        name={"Filter"}
        type={"radio"}
        checked={props.currentFilterOptions.status === StatusFilter.FAILED}
        onClick={() => props.statusFilterChanged(StatusFilter.FAILED)}
        onChange={(e) => {}}
      />
      <Form.Check
        inline
        id="Success"
        label="Success"
        name={"Filter"}
        type={"radio"}
        checked={props.currentFilterOptions.status === StatusFilter.SUCCESS}
        onClick={() => props.statusFilterChanged(StatusFilter.SUCCESS)}
        onChange={(e) => {}}
      />
      <Form.Check
        inline
        id="Running"
        label="Running"
        name={"Filter"}
        type={"radio"}
        checked={props.currentFilterOptions.status === StatusFilter.RUNNING}
        onClick={() => props.statusFilterChanged(StatusFilter.RUNNING)}
        onChange={(e) => {}}
      />
      <Form.Check
        inline
        id="Not Started"
        label={"Not Started"}
        name={"Filter"}
        type={"radio"}
        checked={props.currentFilterOptions.status === StatusFilter.NOT_STARTED}
        onClick={() => props.statusFilterChanged(StatusFilter.NOT_STARTED)}
        onChange={(e) => {}}
      />
    </div>
  );
}

export default FilterControls;
