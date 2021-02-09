import { useCallback, useState } from "react";
import { Page } from "./Page";
import { PageRequest } from "./PageRequest";
interface ControllablePage {
  page_number: number;
  page_size: number;
  total_pages: number;
}
interface PaginationControls {
  currentPage: ControllablePage;
  elementsPerPage: number;
  setElementsPerPage: (elements: number) => void;
  nextPage: () => void;
  previousPage: () => void;
  isFirstPage: () => boolean;
  isLastPage: () => boolean;
}

export function usePagination(
  initialPage: ControllablePage,
  initialElementsPerPage: number,
  pageChangedCallback: (pageRequest: PageRequest) => void
): PaginationControls {
  const [currentPage, setCurrentPage] = useState<ControllablePage>(initialPage);
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
    const newPage: ControllablePage = {
      page_number: currentPage.page_number + 1,
      page_size: elementsPerPage,
      total_pages: currentPage.total_pages,
    };
    setCurrentPage(newPage);
    pageChangedCallback(newPage);
  };

  const previousPage = () => {
    if (isFirstPage()) {
      return;
    }
    const newPage: ControllablePage = {
      page_number: currentPage.page_number - 1,
      page_size: elementsPerPage,
      total_pages: currentPage.total_pages,
    };
    setCurrentPage(newPage);
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
