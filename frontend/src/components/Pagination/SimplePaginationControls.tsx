import React from "react";
import { Page, PageRequest } from "./Page";
import { usePagination } from "./usePagination";
import styles from "./SimplePaginationControl.module.scss";
import { ChevronRight, ChevronLeft } from "react-bootstrap-icons";
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
        <button
          aria-label={"Previous"}
          disabled={controls.isFirstPage()}
          onClick={() => controls.previousPage()}
        >
          <ChevronLeft />
          Previous
        </button>
        <button
          aria-label={"Next Page"}
          disabled={controls.isLastPage()}
          onClick={() => controls.nextPage()}
        >
          Next Page <ChevronRight />
        </button>
      </div>
    </div>
  );
};

export default SimplePaginationControls;
