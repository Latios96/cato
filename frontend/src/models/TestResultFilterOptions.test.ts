import {
  StatusFilter,
  TestResultFilterOptions,
} from "./TestResultFilterOptions";

describe("TestResultFilterOptions", () => {
  it("should construct with default status filter NONE", () => {
    const filterOptions = new TestResultFilterOptions();

    expect(filterOptions.status).toBe(StatusFilter.NONE);
  });

  it("should construct with supplied status filter", () => {
    const filterOptions = new TestResultFilterOptions(StatusFilter.FAILED);

    expect(filterOptions.status).toBe(StatusFilter.FAILED);
  });
});
