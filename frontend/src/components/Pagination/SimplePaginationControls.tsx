import React from "react";
import { Pagination } from "react-bootstrap";
import {
  firstEntityOnPage,
  lastEntityOnPage,
  Page,
  PageRequest,
  totalEntities,
} from "./Page";
import { usePagination } from "./usePagination";

interface Props<T extends Object> {
  currentPage: Page<T>;
}

const SimplePaginationControls = <T extends Object>(props: Props<T>) => {
  const controls = usePagination(
    props.currentPage,
    props.currentPage.page_size,
    (pageRequest: PageRequest) => {}
  );

  return (
    <div>
      <span>
        {firstEntityOnPage(controls.currentPage)}-
        {lastEntityOnPage(controls.currentPage)} of{" "}
        {totalEntities(controls.currentPage)}
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
  );
};

export default SimplePaginationControls;
