import { testResultFilterOptionsFromQueryString } from "./filterOptionUtils";
import { StatusFilter, FilterOptions } from "../models/FilterOptions";

describe("filterOptionUtils", () => {
  describe("testResultFilterOptionsFromQueryString", () => {
    it("should parse provided value", () => {
      const filterOptions = testResultFilterOptionsFromQueryString(
        "statusFilter=FAILED"
      );

      expect(filterOptions).toStrictEqual(
        new FilterOptions(StatusFilter.FAILED)
      );
    });
    it("should use default", () => {
      const filterOptions = testResultFilterOptionsFromQueryString("asdf=test");

      expect(filterOptions).toStrictEqual(new FilterOptions(StatusFilter.NONE));
    });
  });
});
