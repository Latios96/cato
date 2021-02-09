import { renderHook } from "@testing-library/react-hooks";
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
      const lastPageFittingExactly = {
        page_number: 10,
        page_size: 1,
        total_pages: 10,
        entities: [{ id: 1, name: "test" }],
      };
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
      const lastPageWithSomePlaces = {
        page_number: 10,
        page_size: 5,
        total_pages: 10,
        entities: [{ id: 1, name: "test" }],
      };
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
      const lastPageWithSomePlaces = {
        page_number: 5,
        page_size: 1,
        total_pages: 10,
        entities: [{ id: 1, name: "test" }],
      };
      const { result } = renderHook(() =>
        usePagination(
          lastPageWithSomePlaces,
          10,
          (pageRequest: PageRequest) => {}
        )
      );

      expect(result.current.isFirstPage()).toBe(false);
      expect(result.current.isLastPage()).toBe(false);
    });
  });

  describe("change page", () => {
    it("should change nothing when calling previos page on first page", () => {});
    it("should change nothing when calling next page on last page", () => {});
    it("should change to next page when calling next page on first page", () => {});
    it("should change to previous page when calling previous page on last page", () => {});
    it("should change to next page when calling next page on middle page", () => {});
    it("should change to previous page when calling previous page on middle page", () => {});
  });

  describe("change elements per page", () => {
    //first page
    //last page
  });
});
