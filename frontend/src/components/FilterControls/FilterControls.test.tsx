import each from "jest-each";
import FilterControls from "./FilterControls";
import { render } from "@testing-library/react";
import { StatusFilter, FilterOptions } from "../../models/FilterOptions";

describe("FilterControls", () => {
  each([
    ["All", StatusFilter.NONE],
    ["Failed", StatusFilter.FAILED],
    ["Success", StatusFilter.SUCCESS],
    ["Running", StatusFilter.RUNNING],
    ["Not Started", StatusFilter.NOT_STARTED],
  ]).it(
    "should report the correct status selection when clicking",
    (label: string, status: StatusFilter) => {
      const filterChangedCallback = jest.fn();
      const rendered = render(
        <FilterControls
          currentFilterOptions={new FilterOptions(StatusFilter.NONE)}
          statusFilterChanged={filterChangedCallback}
        />
      );

      rendered.getByText(label).click();

      expect(filterChangedCallback).toBeCalledWith(status);
    }
  );

  each([
    ["All", StatusFilter.NONE],
    ["Failed", StatusFilter.FAILED],
    ["Success", StatusFilter.SUCCESS],
    ["Running", StatusFilter.RUNNING],
    ["Not Started", StatusFilter.NOT_STARTED],
  ]).it(
    "should select the correct radio button",
    (label: string, status: StatusFilter) => {
      const filterChangedCallback = jest.fn();
      const rendered = render(
        <FilterControls
          currentFilterOptions={new FilterOptions(status)}
          statusFilterChanged={filterChangedCallback}
        />
      );

      const byText = rendered.getByLabelText(label);

      expect(byText).toBeChecked();
    }
  );
});
