import {
  ControllablePage,
  firstEntityOnPage,
  lastEntityOnPage,
  requestFirstPageOfSize,
  totalPages,
} from "./Page";
import each from "jest-each";

describe("PageRequest", () => {
  it("should create first page correctly", () => {
    const firstPageRequest = requestFirstPageOfSize(10);

    expect(firstPageRequest).toStrictEqual({ page_number: 1, page_size: 10 });
  });
});

describe("Page", () => {
  each([
    [
      1,
      {
        page_number: 1,
        page_size: 10,
        total_pages: 10,
      },
    ],
    [
      11,
      {
        page_number: 2,
        page_size: 10,
        total_pages: 10,
      },
    ],
  ]).it(
    "should return first entity on page %s correctly",
    (firstEntity: number, page: ControllablePage) => {
      const first = firstEntityOnPage(page);

      expect(first).toBe(firstEntity);
    }
  );
  each([
    [
      10,
      {
        page_number: 1,
        page_size: 10,
        total_entity_count: 100,
      },
    ],
    [
      20,
      {
        page_number: 2,
        page_size: 10,
        total_entity_count: 20,
      },
    ],
    [
      18,
      {
        page_number: 2,
        page_size: 10,
        total_entity_count: 18,
      },
    ],
  ]).it(
    "should return last entity on page %s correctly",
    (lastEntity: number, page: ControllablePage) => {
      const first = lastEntityOnPage(page);

      expect(first).toBe(lastEntity);
    }
  );
  each([
    [0, 1],
    [1, 1],
    [9, 1],
    [10, 1],
    [11, 2],
    [50, 5],
    [100, 10],
  ]).it(
    "should calculate total page count for %s entites correctly",
    (totalEntityCount: number, totalPageCount: number) => {
      const first = totalPages({
        page_number: 1,
        page_size: 10,
        total_entity_count: totalEntityCount,
      });

      expect(first).toBe(totalPageCount);
    }
  );
});
