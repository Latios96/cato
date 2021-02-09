import React from "react";
import { Pagination } from "react-bootstrap";
import { Page } from "./Page";
import { usePagination } from "./usePagination";
import { PageRequest } from "./PageRequest";

interface Props<T extends Object> {
  currentPage: Page<T>;
}

const SimplePaginationControls = <T extends Object>(props: Props<T>) => {
  const usePaginationControls = usePagination(
    props.currentPage,
    props.currentPage.page_size,
    (pageRequest: PageRequest) => {}
  );
  return (
    <div>
      <Pagination size={"sm"}>
        <Pagination.Prev
          role={"previous"}
          disabled={usePaginationControls.isFirstPage()}
        />
        <Pagination.Next
          role={"next"}
          disabled={usePaginationControls.isLastPage()}
        />
      </Pagination>
    </div>
  );
};

export default SimplePaginationControls;
