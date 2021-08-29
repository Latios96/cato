import { FilterOptions, StatusFilter } from "./FilterOptions";

describe("FilterOptions", () => {
  it("should construct with default status filter NONE", () => {
    const filterOptions = new FilterOptions();

    expect(filterOptions.status).toBe(StatusFilter.NONE);
  });

  it("should construct with supplied status filter", () => {
    const filterOptions = new FilterOptions(StatusFilter.FAILED);

    expect(filterOptions.status).toBe(StatusFilter.FAILED);
  });
});
