import React from "react";
import { Pagination } from "react-bootstrap";
import { firstEntityOnPage, lastEntityOnPage, Page, PageRequest } from "./Page";
import { usePagination } from "./usePagination";
import styles from "./SimplePaginationControl.module.scss";

interface Props<T extends Object> {
  currentPage: Page<T>;
  pageChangedCallback: (pageRequest: PageRequest) => void;
}

const SimplePaginationControls = <T extends Object>(props: Props<T>) => {
  const controls = usePagination(
    props.currentPage,
    props.currentPage.page_size,
    props.pageChangedCallback
  );

  return (
    <div className={styles.paginationControlContainer}>
      <div className={styles.controls}>
        <span className={styles.elementsOnPage}>
          {firstEntityOnPage(controls.currentPage)}-
          {lastEntityOnPage(controls.currentPage)} of{" "}
          {controls.currentPage.total_entity_count}
        </span>
        <Pagination size={"sm"}>
          <Pagination.Prev
            role={"previous"}
            disabled={controls.isFirstPage()}
            onClick={() => controls.previousPage()}
          />
          <Pagination.Next
            role={"next"}
            disabled={controls.isLastPage()}
            onClick={() => controls.nextPage()}
          />
        </Pagination>
      </div>
    </div>
  );
};

export default SimplePaginationControls;
