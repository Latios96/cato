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

    expect(firstPageRequest).toStrictEqual({ pageNumber: 1, pageSize: 10 });
  });
});

describe("Page", () => {
  each([
    [
      1,
      {
        pageNumber: 1,
        pageSize: 10,
        totaPages: 10,
      },
    ],
    [
      11,
      {
        pageNumber: 2,
        pageSize: 10,
        totalPages: 10,
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
        pageNumber: 1,
        pageSize: 10,
        totalEntityCount: 100,
      },
    ],
    [
      20,
      {
        pageNumber: 2,
        pageSize: 10,
        totalEntityCount: 20,
      },
    ],
    [
      18,
      {
        pageNumber: 2,
        pageSize: 10,
        totalEntityCount: 18,
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
        pageNumber: 1,
        pageSize: 10,
        totalEntityCount: totalEntityCount,
      });

      expect(first).toBe(totalPageCount);
    }
  );
});
