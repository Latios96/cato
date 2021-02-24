import { useState } from "react";
import { ControllablePage, PageRequest, totalPages } from "./Page";

interface PaginationControls {
  currentPage: ControllablePage;
  elementsPerPage: number;
  changeCurrentElementsPerPage: (elements: number) => void;
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
    return currentPage.page_number === totalPages(currentPage);
  };

  const nextPage = () => {
    if (isLastPage()) {
      return;
    }
    const newPage: ControllablePage = {
      page_number: currentPage.page_number + 1,
      page_size: elementsPerPage,
      total_entity_count: currentPage.total_entity_count,
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
      total_entity_count: currentPage.total_entity_count,
    };
    setCurrentPage(newPage);
    pageChangedCallback(newPage);
  };

  return {
    currentPage: currentPage,
    elementsPerPage: elementsPerPage,
    changeCurrentElementsPerPage: (count: number) => {
      setElementsPerPage(count);
      const newPage = {
        page_number: currentPage.page_number,
        page_size: count,
        total_entity_count: currentPage.total_entity_count,
      };
      setCurrentPage(newPage);
      pageChangedCallback(newPage);
    },
    nextPage: nextPage,
    previousPage: previousPage,
    isFirstPage: isFirstPage,
    isLastPage: isLastPage,
  };
}
