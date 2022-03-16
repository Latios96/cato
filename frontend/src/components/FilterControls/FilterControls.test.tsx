import each from "jest-each";
import FilterControls from "./FilterControls";
import { fireEvent, render } from "@testing-library/react";
import { FilterOptions } from "../../models/FilterOptions";
import {
  StatusFilter,
  TestFailureReason,
} from "../../catoapimodels/catoapimodels";

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
          filterOptionsChanged={filterChangedCallback}
        />
      );

      rendered.getByText(label).click();

      expect(filterChangedCallback).toBeCalledWith({
        status,
        failureReason: undefined,
      });
    }
  );

  describe("failure reason filters should be only displayed if statusFilter is FAILED", () => {
    it("should not display failure reasons", () => {
      const filterChangedCallback = jest.fn();

      const rendered = render(
        <FilterControls
          currentFilterOptions={new FilterOptions(StatusFilter.NONE)}
          filterOptionsChanged={filterChangedCallback}
        />
      );

      expect(rendered.queryByText("Failure Reason")).not.toBeInTheDocument();
    });

    it("should display failure reasons", () => {
      const filterChangedCallback = jest.fn();

      const rendered = render(
        <FilterControls
          currentFilterOptions={new FilterOptions(StatusFilter.FAILED)}
          filterOptionsChanged={filterChangedCallback}
        />
      );
      expect(rendered.getByText("Failure Reason")).toBeInTheDocument();
    });

    it("should not display failure reasons because its disabled", () => {
      const filterChangedCallback = jest.fn();

      const rendered = render(
        <FilterControls
          currentFilterOptions={new FilterOptions(StatusFilter.FAILED)}
          filterOptionsChanged={filterChangedCallback}
          failureReasonIsNotFilterable={true}
        />
      );

      expect(rendered.queryByText("Failure Reason")).not.toBeInTheDocument();
    });
  });

  each([
    ["None", undefined],
    [
      TestFailureReason.EXIT_CODE_NON_ZERO,
      TestFailureReason.EXIT_CODE_NON_ZERO,
    ],
    [
      TestFailureReason.EXIT_CODE_NON_ZERO,
      TestFailureReason.EXIT_CODE_NON_ZERO,
    ],
    [
      TestFailureReason.EXIT_CODE_NON_ZERO,
      TestFailureReason.EXIT_CODE_NON_ZERO,
    ],
    [
      TestFailureReason.EXIT_CODE_NON_ZERO,
      TestFailureReason.EXIT_CODE_NON_ZERO,
    ],
    [
      TestFailureReason.REFERENCE_AND_OUTPUT_IMAGE_MISSING,
      TestFailureReason.REFERENCE_AND_OUTPUT_IMAGE_MISSING,
    ],
    [TestFailureReason.TIMED_OUT, TestFailureReason.TIMED_OUT],
  ]).it(
    "should report the correct failureReason selection when clicking",
    (value: string, failureReason?: TestFailureReason) => {
      const filterChangedCallback = jest.fn();
      const rendered = render(
        <FilterControls
          currentFilterOptions={
            new FilterOptions(StatusFilter.FAILED, failureReason)
          }
          filterOptionsChanged={filterChangedCallback}
        />
      );

      fireEvent.change(rendered.getByLabelText("Failure Reason"), {
        target: { value },
      });

      expect(filterChangedCallback).toBeCalledWith({
        status: StatusFilter.FAILED,
        failureReason,
      });
    }
  );

  it("should default to failure reason filter None when switching to statusFilter FAILED", () => {
    const filterChangedCallback = jest.fn();
    const rendered = render(
      <FilterControls
        currentFilterOptions={new FilterOptions(StatusFilter.NONE)}
        filterOptionsChanged={filterChangedCallback}
      />
    );

    rendered.getByText("Failed").click();

    expect(filterChangedCallback).toBeCalledWith({
      status: StatusFilter.FAILED,
      failureReason: undefined,
    });
  });

  it("should remove failure reason filter when switching away from FAILED", () => {
    const filterChangedCallback = jest.fn();
    const rendered = render(
      <FilterControls
        currentFilterOptions={
          new FilterOptions(StatusFilter.FAILED, TestFailureReason.TIMED_OUT)
        }
        filterOptionsChanged={filterChangedCallback}
      />
    );

    rendered.getByText("Success").click();

    expect(filterChangedCallback).toBeCalledWith({
      status: StatusFilter.SUCCESS,
      failureReason: undefined,
    });
  });

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
          filterOptionsChanged={filterChangedCallback}
        />
      );

      const byText = rendered.getByLabelText(label);

      expect(byText).toBeChecked();
    }
  );
});
