import { filterOptionsFromQueryString } from "./filterOptionUtils";
import { FilterOptions, StatusFilter } from "../models/FilterOptions";

describe("filterOptionUtils", () => {
  describe("filterOptionsFromQueryString", () => {
    it("should parse provided value", () => {
      const filterOptions = filterOptionsFromQueryString("statusFilter=FAILED");

      expect(filterOptions).toStrictEqual(
        new FilterOptions(StatusFilter.FAILED)
      );
    });

    it("should use default", () => {
      const filterOptions = filterOptionsFromQueryString("asdf=test");

      expect(filterOptions).toStrictEqual(new FilterOptions(StatusFilter.NONE));
    });
  });
});
