import { useState } from "react";
import { Page } from "./Page";
import { PageRequest } from "./PageRequest";

interface PaginationControls<T extends Object> {
  currentPage: Page<T>;
  elementsPerPage: number;
  setElementsPerPage: (elements: number) => void;
  nextPage: () => void;
  previousPage: () => void;
  isFirstPage: () => boolean;
  isLastPage: () => boolean;
}

export function usePagination<T extends Object>(
  initialPage: Page<T>,
  initialElementsPerPage: number,
  pageChangedCallback: (pageRequest: PageRequest) => void
): PaginationControls<T> {
  const [currentPage, setCurrentPage] = useState<Page<T>>(initialPage);
  const [elementsPerPage, setElementsPerPage] = useState<number>(
    initialElementsPerPage
  );

  const isFirstPage = (): boolean => {
    return currentPage.page_number === 1;
  };

  const isLastPage = (): boolean => {
    return currentPage.page_number === currentPage.total_pages;
  };

  const nextPage = () => {
    if (isLastPage()) {
      return;
    }
    const newPage: PageRequest = {
      page_number: currentPage.page_number + 1,
      page_size: elementsPerPage,
    };
    pageChangedCallback(newPage);
  };

  const previousPage = () => {
    if (isFirstPage()) {
      return;
    }
    const newPage: PageRequest = {
      page_number: currentPage.page_number - 1,
      page_size: elementsPerPage,
    };
    pageChangedCallback(newPage);
  };

  return {
    currentPage: currentPage,
    elementsPerPage: elementsPerPage,
    setElementsPerPage: setElementsPerPage,
    nextPage: nextPage,
    previousPage: previousPage,
    isFirstPage: isFirstPage,
    isLastPage: isLastPage,
  };
}
