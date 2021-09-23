import TestResultComparisonResult from "./TestResultComparisonResult";
import { fireEvent, render, waitFor } from "@testing-library/react";
import { ComparisonMethodDto } from "../../catoapimodels";
import axios from "axios";
jest.mock("axios");

describe("TestResultComparisonResult", () => {
  it("should display a placeholder for non existing comparison settings", () => {
    const rendered = render(
      <TestResultComparisonResult
        testResult={{ comparison_settings: null, error_value: null }}
      />
    );
    expect(rendered.getByTestId("comparison-method-method")).toHaveTextContent(
      "—"
    );
    expect(
      rendered.getByTestId("comparison-method-threshold")
    ).toHaveTextContent("—");
  });

  it("should display a placeholder for non existing error value", () => {
    const rendered = render(
      <TestResultComparisonResult
        testResult={{ comparison_settings: null, error_value: null }}
      />
    );
    expect(rendered.getByTestId("error-value")).toHaveTextContent("—");
  });

  it("should render the comparison settings", () => {
    const rendered = render(
      <TestResultComparisonResult
        testResult={{
          comparison_settings: {
            method: ComparisonMethodDto.SSIM,
            threshold: 0.9,
          },
          error_value: null,
        }}
      />
    );
    expect(rendered.getByTestId("comparison-method-method")).toHaveTextContent(
      "SSIM"
    );
    expect(
      rendered.getByTestId("comparison-method-threshold")
    ).toHaveTextContent("0.9");
  });

  it("should render the error value", () => {
    const rendered = render(
      <TestResultComparisonResult
        testResult={{ comparison_settings: null, error_value: 1.5 }}
      />
    );
    expect(rendered.getByTestId("error-value")).toHaveTextContent("1.5");
  });
  // todo check if can be edited
  it("should display the edit button by default", () => {
    const rendered = render(
      <TestResultComparisonResult
        testResult={{
          comparison_settings: {
            method: ComparisonMethodDto.SSIM,
            threshold: 0.9,
          },
          error_value: 1.5,
        }}
      />
    );
    expect(rendered.getByText("Edit")).toBeInTheDocument();
    expect(rendered.getByText("Edit")).toBeEnabled();
  });
  it("should switch to edit mode when clicking the edit button", () => {
    const rendered = render(
      <TestResultComparisonResult
        testResult={{
          comparison_settings: {
            method: ComparisonMethodDto.SSIM,
            threshold: 0.9,
          },
          error_value: 1.5,
        }}
      />
    );

    fireEvent.click(rendered.getByText("Edit"));

    expect(rendered.queryByText("Edit")).not.toBeInTheDocument();
    expect(rendered.getByText("OK")).toBeEnabled();
    expect(rendered.getByText("Cancel")).toBeEnabled();
    expect(
      rendered.getByTestId("edit-comparison-settings-method")
    ).toBeInTheDocument();
    expect(
      rendered.getByTestId("edit-comparison-settings-threshold")
    ).toBeInTheDocument();
  });

  it("should display the present values after canceling editing", () => {
    const rendered = render(
      <TestResultComparisonResult
        testResult={{
          comparison_settings: {
            method: ComparisonMethodDto.SSIM,
            threshold: 0.9,
          },
          error_value: 1.5,
        }}
      />
    );

    fireEvent.click(rendered.getByText("Edit"));
    fireEvent.change(
      rendered.getByTestId("edit-comparison-settings-threshold"),
      {
        target: { value: "0.5" },
      }
    );
    fireEvent.click(rendered.getByText("Cancel"));

    expect(rendered.getByTestId("error-value")).toHaveTextContent("1.5");
    expect(
      rendered.getByTestId("comparison-method-threshold")
    ).toHaveTextContent("0.5");
    expect(rendered.getByTestId("comparison-method-method")).toHaveTextContent(
      "SSIM"
    );
  });

  it("should match the error value when pressing the match button", () => {
    const rendered = render(
      <TestResultComparisonResult
        testResult={{
          comparison_settings: {
            method: ComparisonMethodDto.SSIM,
            threshold: 0.9,
          },
          error_value: 1.5,
        }}
      />
    );

    fireEvent.click(rendered.getByText("Edit"));
    fireEvent.click(rendered.getByText("match error"));

    expect(
      rendered.getByTestId("edit-comparison-settings-threshold")
    ).toHaveValue(1.5);
  });

  it("should update the value in backend when pressing OK", () => {
    const rendered = render(
      <TestResultComparisonResult
        testResult={{
          id: 1,
          comparison_settings: {
            method: ComparisonMethodDto.SSIM,
            threshold: 0.9,
          },
          error_value: 1.5,
        }}
      />
    );
    axios.post.mockImplementationOnce(() => Promise.resolve({}));

    fireEvent.click(rendered.getByText("Edit"));
    fireEvent.change(
      rendered.getByTestId("edit-comparison-settings-threshold"),
      {
        target: { value: "0.5" },
      }
    );
    fireEvent.click(rendered.getByText("OK"));

    expect(axios.post).toHaveBeenCalledWith(
      "/api/v1/test_edits/comparison_settings",
      {
        test_result_id: 1,
        new_value: {
          method: "SSIM",
          threshold: 0.5,
        },
      }
    );
  });
});
