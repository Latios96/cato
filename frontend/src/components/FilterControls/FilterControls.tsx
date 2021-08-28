import React from "react";
import { Form } from "react-bootstrap";
import { StatusFilter } from "../../catoapimodels";
import styles from "./FilterControls.module.scss";
interface Props {
  currentFilter: StatusFilter;
  filterChanged: (filter: StatusFilter) => void;
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
        checked={props.currentFilter === StatusFilter.NONE}
        onClick={() => props.filterChanged(StatusFilter.NONE)}
        onChange={(e) => {}}
      />
      <Form.Check
        inline
        id="Failed"
        label="Failed"
        name={"Filter"}
        type={"radio"}
        checked={props.currentFilter === StatusFilter.FAILED}
        onClick={() => props.filterChanged(StatusFilter.FAILED)}
        onChange={(e) => {}}
      />
      <Form.Check
        inline
        id="Success"
        label="Success"
        name={"Filter"}
        type={"radio"}
        checked={props.currentFilter === StatusFilter.SUCCESS}
        onClick={() => props.filterChanged(StatusFilter.SUCCESS)}
        onChange={(e) => {}}
      />
      <Form.Check
        inline
        id="Running"
        label="Running"
        name={"Filter"}
        type={"radio"}
        checked={props.currentFilter === StatusFilter.RUNNING}
        onClick={() => props.filterChanged(StatusFilter.RUNNING)}
        onChange={(e) => {}}
      />
      <Form.Check
        inline
        id="Not Started"
        label={"Not Started"}
        name={"Filter"}
        type={"radio"}
        checked={props.currentFilter === StatusFilter.NOT_STARTED}
        onClick={() => props.filterChanged(StatusFilter.NOT_STARTED)}
        onChange={(e) => {}}
      />
    </div>
  );
}

export default FilterControls;
