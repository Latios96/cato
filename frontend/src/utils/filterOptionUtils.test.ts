import { filterOptionsFromQueryString } from "./filterOptionUtils";
import { FilterOptions } from "../models/FilterOptions";
import { TestFailureReasonDto } from "../catoapimodels";
import { StatusFilter } from "../catoapimodels/catoapimodels";

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

    it("should parse failureReason", () => {
      const filterOptions = filterOptionsFromQueryString(
        "statusFilter=FAILED&failureReasonFilter=TIMED_OUT"
      );

      expect(filterOptions).toStrictEqual(
        new FilterOptions(StatusFilter.FAILED, TestFailureReasonDto.TIMED_OUT)
      );
    });

    it("should not parse failureReason if statusFilter is not FAILED", () => {
      const filterOptions = filterOptionsFromQueryString(
        "statusFilter=SUCCESS&failureReasonFilter=TIMED_OUT"
      );

      expect(filterOptions).toStrictEqual(
        new FilterOptions(StatusFilter.SUCCESS)
      );
    });
  });
});
