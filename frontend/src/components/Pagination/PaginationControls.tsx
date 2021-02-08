import React from "react";
import { Pagination } from "react-bootstrap";
import { Page } from "./Page";

interface Props<T extends Object> {
  currentPage: Page<T>;
}

const PaginationControls = <T extends Object>(props: Props<T>) => {
  return (
    <Pagination size={"sm"}>
      <Pagination.First />
      <Pagination.Prev />
      <Pagination.Item active>{1}</Pagination.Item>
      <Pagination.Item>{2}</Pagination.Item>
      <Pagination.Item>{3}</Pagination.Item>
      <Pagination.Item>{4}</Pagination.Item>
      <Pagination.Item>{5}</Pagination.Item>
      <Pagination.Ellipsis />
      <Pagination.Item>{20}</Pagination.Item>
      <Pagination.Next />
      <Pagination.Last />
    </Pagination>
  );
};

export default PaginationControls;
