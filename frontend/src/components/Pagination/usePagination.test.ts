import { act, renderHook } from "@testing-library/react-hooks";
import { usePagination } from "./usePagination";
import { PageRequest } from "./PageRequest";

const smallPage = {
  page_number: 1,
  page_size: 10,
  total_pages: 1,
  entities: [{ id: 1, name: "test" }],
};

const firstPage = {
  page_number: 1,
  page_size: 10,
  total_pages: 10,
  entities: [{ id: 1, name: "test" }],
};

const middlePage = {
  page_number: 5,
  page_size: 1,
  total_pages: 10,
  entities: [{ id: 1, name: "test" }],
};

const lastPageWithSomePlaces = {
  page_number: 10,
  page_size: 5,
  total_pages: 10,
  entities: [{ id: 1, name: "test" }],
};

const lastPageFittingExactly = {
  page_number: 10,
  page_size: 1,
  total_pages: 10,
  entities: [{ id: 1, name: "test" }],
};

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
          10,
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

      expect(result.current.currentPage).toStrictEqual({
        page_number: 2,
        page_size: firstPage.page_size,
        total_pages: firstPage.total_pages,
      });
      expect(mockCallBack.mock.calls.length).toEqual(1);
    });

    it("should change to previous page when calling previous page on last page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(lastPageFittingExactly, 1, mockCallBack)
      );

      act(() => {
        result.current.previousPage();
      });

      expect(result.current.currentPage).toStrictEqual({
        page_number: 9,
        page_size: lastPageFittingExactly.page_size,
        total_pages: lastPageFittingExactly.total_pages,
      });
      expect(mockCallBack.mock.calls.length).toEqual(1);
    });

    it("should change to next page when calling next page on middle page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(middlePage, middlePage.page_size, mockCallBack)
      );

      act(() => {
        result.current.nextPage();
      });

      expect(result.current.currentPage).toStrictEqual({
        page_number: 6,
        page_size: middlePage.page_size,
        total_pages: middlePage.total_pages,
      });
      expect(mockCallBack.mock.calls.length).toEqual(1);
    });

    it("should change to previous page when calling previous page on middle page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(middlePage, middlePage.page_size, mockCallBack)
      );

      act(() => {
        result.current.previousPage();
      });

      expect(result.current.currentPage).toStrictEqual({
        page_number: 4,
        page_size: middlePage.page_size,
        total_pages: middlePage.total_pages,
      });
      expect(mockCallBack.mock.calls.length).toEqual(1);
    });
  });

  describe("change elements per page", () => {
    it("should change elements per page", () => {
      const mockCallBack = jest.fn();
      const { result } = renderHook(() =>
        usePagination(smallPage, middlePage.page_size, mockCallBack)
      );

      act(() => {
        result.current.changeCurrentElementsPerPage(11);
      });

      expect(result.current.currentPage).toStrictEqual({
        page_number: smallPage.page_number,
        page_size: 11,
        total_pages: smallPage.total_pages,
      });
      expect(mockCallBack.mock.calls.length).toEqual(1);
    });
  });
});
