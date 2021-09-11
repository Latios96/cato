import TestResultComparisonResult from "./TestResultComparisonResult";
import { render } from "@testing-library/react";
import { ComparisonMethodDto } from "../../catoapimodels";

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
});
