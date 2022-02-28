import { fireEvent, render } from "@testing-library/react";
import { ComparisonMethodDto, TestResultDto } from "../../catoapimodels";
import TestResultComparisonResultImpl from "./TestResultComparisonResultImpl";
import { ActionType, getInitialState, State } from "./reducer";

describe("TestResultComparisonResultImpl", () => {
  const setup = (
    testResult: Pick<TestResultDto, "comparison_settings" | "error_value">,
    state?: Partial<State>
  ) => {
    const dispatch = jest.fn();
    const updateComparisonSettings = jest.fn();
    const rendered = render(
      <TestResultComparisonResultImpl
        state={{ ...getInitialState(testResult), ...state }}
        testResult={testResult}
        dispatch={dispatch}
        updateComparisonSettings={updateComparisonSettings}
      />
    );
    return { rendered, dispatch, updateComparisonSettings };
  };

  it("should display a placeholder for non existing comparison settings and error value", () => {
    const { rendered } = setup({
      comparison_settings: null,
      error_value: null,
    });

    expect(rendered.getByTestId("comparison-method-method")).toHaveTextContent(
      "—"
    );
    expect(
      rendered.getByTestId("comparison-method-threshold")
    ).toHaveTextContent("—");
    expect(rendered.getByTestId("error-value")).toHaveTextContent("—");
  });

  it("should render the comparison settings and error value", () => {
    const { rendered } = setup({
      comparison_settings: {
        method: ComparisonMethodDto.SSIM,
        threshold: 0.9,
      },
      error_value: 1.5,
    });

    expect(rendered.getByTestId("comparison-method-method")).toHaveTextContent(
      "SSIM"
    );
    expect(
      rendered.getByTestId("comparison-method-threshold")
    ).toHaveTextContent("0.9");
    expect(rendered.getByTestId("error-value")).toHaveTextContent("1.5");
  });

  it("should display the edit button disabled by default", () => {
    const { rendered } = setup({
      comparison_settings: {
        method: ComparisonMethodDto.SSIM,
        threshold: 0.9,
      },
      error_value: 1.5,
    });

    expect(rendered.getByText("Edit")).toBeInTheDocument();
    expect(rendered.getByText("Edit")).not.toBeEnabled();
  });

  it("should display the edit button enabled", () => {
    const { rendered } = setup(
      {
        comparison_settings: {
          method: ComparisonMethodDto.SSIM,
          threshold: 0.9,
        },
        error_value: 1.5,
      },
      { isEditable: { can_edit: true } }
    );

    expect(rendered.getByText("Edit")).toBeInTheDocument();
    expect(rendered.getByText("Edit")).not.toBeEnabled();
  });
  it("should display the edit button disabled because its not editable", () => {
    const { rendered } = setup(
      {
        comparison_settings: {
          method: ComparisonMethodDto.SSIM,
          threshold: 0.9,
        },
        error_value: 1.5,
      },
      { isEditable: { can_edit: false, message: "can not be edited" } }
    );

    expect(rendered.getByText("Edit")).toBeInTheDocument();
    expect(rendered.getByText("Edit")).not.toBeEnabled();
  });

  it("should display the edit button disabled because its editableChecking", () => {
    const { rendered } = setup(
      {
        comparison_settings: {
          method: ComparisonMethodDto.SSIM,
          threshold: 0.9,
        },
        error_value: 1.5,
      },
      {
        isEditable: undefined,
        isEditableChecking: true,
      }
    );

    expect(rendered.getByText("Edit")).toBeInTheDocument();
    expect(rendered.getByText("Edit")).not.toBeEnabled();
  });

  it("should dispatch START_EDITING when clicking edit button", () => {
    const { rendered, dispatch } = setup(
      {
        comparison_settings: {
          method: ComparisonMethodDto.SSIM,
          threshold: 0.9,
        },
        error_value: 1.5,
      },
      { isEditable: { can_edit: true }, isEditableChecking: false }
    );

    fireEvent.click(rendered.getByText("Edit"));

    expect(dispatch).toBeCalledWith({ type: ActionType.START_EDITING });
  });

  it("should display edit inputs and buttons when editing", () => {
    const { rendered } = setup(
      {
        comparison_settings: {
          method: ComparisonMethodDto.SSIM,
          threshold: 0.9,
        },
        error_value: 1.5,
      },
      { isEditable: { can_edit: true }, isEditing: true }
    );

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

  it("should dispatch changed threshold when editing", () => {
    const { rendered, dispatch } = setup(
      {
        comparison_settings: {
          method: ComparisonMethodDto.SSIM,
          threshold: 0.9,
        },
        error_value: 1.5,
      },
      { isEditable: { can_edit: true }, isEditing: true }
    );

    fireEvent.change(
      rendered.getByTestId("edit-comparison-settings-threshold"),
      {
        target: { value: "0.5" },
      }
    );

    expect(dispatch).toBeCalledWith({
      type: ActionType.SET_CURRENT_THRESHOLD,
      payload: "0.5",
    });
  });

  it("should dispatch CANCEL with when canceling", () => {
    const { rendered, dispatch } = setup(
      {
        comparison_settings: {
          method: ComparisonMethodDto.SSIM,
          threshold: 0.9,
        },
        error_value: 1.5,
      },
      { isEditable: { can_edit: true }, isEditing: true }
    );

    fireEvent.click(rendered.getByText("Cancel"));

    expect(dispatch).toBeCalledWith({ type: ActionType.CANCEL });
  });

  it("should dispatch error value when pressing the match button", () => {
    const { rendered, dispatch } = setup(
      {
        comparison_settings: {
          method: ComparisonMethodDto.SSIM,
          threshold: 0.9,
        },
        error_value: 1.5,
      },
      { isEditable: { can_edit: true }, isEditing: true }
    );

    fireEvent.click(rendered.getByText("match error"));

    expect(dispatch).toBeCalledWith({
      type: ActionType.SET_CURRENT_THRESHOLD,
      payload: "1.500",
    });
  });

  it("should call update with correct value when pressing OK", () => {
    const { rendered, updateComparisonSettings } = setup(
      {
        comparison_settings: {
          method: ComparisonMethodDto.SSIM,
          threshold: 0.9,
        },
        error_value: 1.5,
      },
      {
        isEditable: { can_edit: true },
        isEditing: true,
        currentThreshold: "0.5",
      }
    );

    fireEvent.click(rendered.getByText("OK"));

    expect(updateComparisonSettings).toBeCalledWith({
      method: "SSIM",
      threshold: 0.5,
    });
  });
});
