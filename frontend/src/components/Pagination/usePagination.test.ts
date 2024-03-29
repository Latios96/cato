import { act, renderHook } from "@testing-library/react-hooks";
import { usePagination } from "./usePagination";
import {
  firstPage,
  lastPageFittingExactly,
  lastPageWithSomePlaces,
  middlePage,
  smallPage,
} from "./PaginationTestData";
import { PageRequest } from "./Page";

describe("usePagination hook", () => {
  it("should have the initial page", () => {
    const { result } = renderHook(() =>
      usePagination(smallPage, 10, (pageRequest: PageRequest) => {})
    );

    expect(result.current.currentPage).toStrictEqual(smallPage);
  });

  describe("first and last page", () => {
    it("should mark a small page as first and last page", () => {
      const { result } = renderHook(() =>
        usePagination(smallPage, 10, (pageRequest: PageRequest) => {})
      );

      expect(result.current.isFirstPage()).toBe(true);
      expect(result.current.isLastPage()).toBe(true);
    });

    it("should mark the page as first page", () => {
      const { result } = renderHook(() =>
        usePagination(firstPage, 10, (pageRequest: PageRequest) => {})
      );

      expect(result.current.isFirstPage()).toBe(true);
      expect(result.current.isLastPage()).toBe(false);
    });

    it("should mark the page as last page when elements fit exactly on page", () => {
      const { result } = renderHook(() =>
        usePagination(
          lastPageFittingExactly,
          10,
          (pageRequest: PageRequest) => {}
        )
      );

      expect(result.current.isFirstPage()).toBe(false);
      expect(result.current.isLastPage()).toBe(true);
    });

    it("should mark the page as last page when page has empty places", () => {
      const { result } = renderHook(() =>
        usePagination(
          lastPageWithSomePlaces,
          5,
          (pageRequest: PageRequest) => {}
        )
      );

      expect(result.current.isFirstPage()).toBe(false);
      expect(result.current.isLastPage()).toBe(true);
    });

    it("should mark middle page as middle page", () => {
      const { result } = renderHook(() =>
        usePagination(middlePage, 10, (pageRequest: PageRequest) => {})
      );

      expect(result.current.isFirstPage()).toBe(false);
      expect(result.current.isLastPage()).toBe(false);
    });
  });

  describe("change page", () => {
    it("should change nothing when calling previous page on small first page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(smallPage, 10, mockCallBack)
      );

      act(() => {
        result.current.previousPage();
      });

      expect(result.current.currentPage).toStrictEqual(smallPage);
      expect(mockCallBack).not.toHaveBeenCalled();
    });

    it("should change nothing when calling next page on small first page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(smallPage, 10, mockCallBack)
      );

      act(() => {
        result.current.nextPage();
      });

      expect(result.current.currentPage).toStrictEqual(smallPage);
      expect(mockCallBack).not.toHaveBeenCalled();
    });

    it("should change nothing when calling previous page on first page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(firstPage, 10, mockCallBack)
      );

      act(() => {
        result.current.previousPage();
      });

      expect(result.current.currentPage).toStrictEqual(firstPage);
      expect(mockCallBack).not.toHaveBeenCalled();
    });

    it("should change nothing when calling next page on last page fitting exactly", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(lastPageFittingExactly, 10, mockCallBack)
      );

      act(() => {
        result.current.nextPage();
      });

      expect(result.current.currentPage).toStrictEqual(lastPageFittingExactly);
      expect(mockCallBack).not.toHaveBeenCalled();
    });

    it("should change nothing when calling next page on last page with some places", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(lastPageWithSomePlaces, 10, mockCallBack)
      );

      act(() => {
        result.current.nextPage();
      });

      expect(result.current.currentPage).toStrictEqual(lastPageWithSomePlaces);
      expect(mockCallBack).not.toHaveBeenCalled();
    });

    it("should change to next page when calling next page on first page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(firstPage, 10, mockCallBack)
      );

      act(() => {
        result.current.nextPage();
      });

      const newPage = {
        pageNumber: 2,
        pageSize: firstPage.pageSize,
        totalEntityCount: firstPage.totalEntityCount,
      };
      expect(result.current.currentPage).toStrictEqual(newPage);
      expect(mockCallBack).toHaveBeenCalledWith(newPage);
    });

    it("should change to previous page when calling previous page on last page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(lastPageFittingExactly, 1, mockCallBack)
      );

      act(() => {
        result.current.previousPage();
      });

      const newPage = {
        pageNumber: 9,
        pageSize: lastPageFittingExactly.pageSize,
        totalEntityCount: lastPageFittingExactly.totalEntityCount,
      };
      expect(result.current.currentPage).toStrictEqual(newPage);
      expect(mockCallBack).toHaveBeenCalledWith(newPage);
    });

    it("should change to next page when calling next page on middle page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(middlePage, middlePage.pageSize, mockCallBack)
      );

      act(() => {
        result.current.nextPage();
      });

      const newPage = {
        pageNumber: 6,
        pageSize: middlePage.pageSize,
        totalEntityCount: middlePage.totalEntityCount,
      };
      expect(result.current.currentPage).toStrictEqual(newPage);
      expect(mockCallBack).toHaveBeenCalledWith(newPage);
    });

    it("should change to previous page when calling previous page on middle page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(middlePage, middlePage.pageSize, mockCallBack)
      );

      act(() => {
        result.current.previousPage();
      });

      const newPage = {
        pageNumber: 4,
        pageSize: middlePage.pageSize,
        totalEntityCount: middlePage.totalEntityCount,
      };
      expect(result.current.currentPage).toStrictEqual(newPage);
      expect(mockCallBack).toHaveBeenCalledWith(newPage);
    });
  });

  describe("change elements per page", () => {
    it("should change elements per page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(smallPage, middlePage.pageSize, mockCallBack)
      );

      act(() => {
        result.current.changeCurrentElementsPerPage(11);
      });

      const newPage = {
        pageNumber: smallPage.pageNumber,
        pageSize: 11,
        totalEntityCount: smallPage.totalEntityCount,
      };
      expect(result.current.currentPage).toStrictEqual(newPage);
      expect(mockCallBack).toHaveBeenCalledWith(newPage);
    });
  });
});
