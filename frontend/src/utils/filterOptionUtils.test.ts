import { testResultFilterOptionsFromQueryString } from "./filterOptionUtils";
import { TestResultFilterOptions } from "../models/TestResultFilterOptions";
import { StatusFilter } from "../catoapimodels/statusFilter";

describe("filterOptionUtils", () => {
  describe("testResultFilterOptionsFromQueryString", () => {
    it("should parse provided value", () => {
      const filterOptions = testResultFilterOptionsFromQueryString(
        "statusFilter=FAILED"
      );

      expect(filterOptions).toStrictEqual(
        new TestResultFilterOptions(StatusFilter.FAILED)
      );
    });
    it("should use default", () => {
      const filterOptions = testResultFilterOptionsFromQueryString("asdf=test");

      expect(filterOptions).toStrictEqual(
        new TestResultFilterOptions(StatusFilter.NONE)
      );
    });
  });
});
