import {
  ControllablePage,
  firstEntityOnPage,
  lastEntityOnPage,
  requestFirstPageOfSize,
  totalEntities,
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
        total_pages: 10,
      },
    ],
    [
      20,
      {
        page_number: 2,
        page_size: 10,
        total_pages: 10,
      },
    ],
  ]).it(
    "should return last entity on page %s correctly",
    (lastEntity: number, page: ControllablePage) => {
      const first = lastEntityOnPage(page);

      expect(first).toBe(lastEntity);
    }
  );
  it("should return total entity count correctly", () => {
    const count = totalEntities({
      page_number: 1,
      page_size: 10,
      total_pages: 10,
    });

    expect(count).toBe(100);
  });
});
