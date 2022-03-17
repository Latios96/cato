import { fireEvent, render } from "@testing-library/react";
import {
  TestResultComparisonResultImpl,
  TestResultDtoComparisonPick,
} from "./TestResultComparisonResultImpl";
import { ActionType, getInitialState, State } from "./reducer";
import { ComparisonMethod } from "../../catoapimodels/catoapimodels";

describe("TestResultComparisonResultImpl", () => {
  const setup = (
    testResult: TestResultDtoComparisonPick,
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
      comparisonSettings: undefined,
      errorValue: undefined,
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
      comparisonSettings: {
        method: ComparisonMethod.SSIM,
        threshold: 0.9,
      },
      errorValue: 1.5,
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
      comparisonSettings: {
        method: ComparisonMethod.SSIM,
        threshold: 0.9,
      },
      errorValue: 1.5,
    });

    expect(rendered.getByText("Edit")).toBeInTheDocument();
    expect(rendered.getByText("Edit")).not.toBeEnabled();
  });

  it("should display the edit button enabled", () => {
    const { rendered } = setup(
      {
        comparisonSettings: {
          method: ComparisonMethod.SSIM,
          threshold: 0.9,
        },
        errorValue: 1.5,
      },
      { isEditable: { canEdit: true } }
    );

    expect(rendered.getByText("Edit")).toBeInTheDocument();
    expect(rendered.getByText("Edit")).not.toBeEnabled();
  });
  it("should display the edit button disabled because its not editable", () => {
    const { rendered } = setup(
      {
        comparisonSettings: {
          method: ComparisonMethod.SSIM,
          threshold: 0.9,
        },
        errorValue: 1.5,
      },
      { isEditable: { canEdit: false, message: "can not be edited" } }
    );

    expect(rendered.getByText("Edit")).toBeInTheDocument();
    expect(rendered.getByText("Edit")).not.toBeEnabled();
  });

  it("should display the edit button disabled because its editableChecking", () => {
    const { rendered } = setup(
      {
        comparisonSettings: {
          method: ComparisonMethod.SSIM,
          threshold: 0.9,
        },
        errorValue: 1.5,
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
        comparisonSettings: {
          method: ComparisonMethod.SSIM,
          threshold: 0.9,
        },
        errorValue: 1.5,
      },
      { isEditable: { canEdit: true }, isEditableChecking: false }
    );

    fireEvent.click(rendered.getByText("Edit"));

    expect(dispatch).toBeCalledWith({ type: ActionType.START_EDITING });
  });

  it("should display edit inputs and buttons when editing", () => {
    const { rendered } = setup(
      {
        comparisonSettings: {
          method: ComparisonMethod.SSIM,
          threshold: 0.9,
        },
        errorValue: 1.5,
      },
      { isEditable: { canEdit: true }, isEditing: true }
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
        comparisonSettings: {
          method: ComparisonMethod.SSIM,
          threshold: 0.9,
        },
        errorValue: 1.5,
      },
      { isEditable: { canEdit: true }, isEditing: true }
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
        comparisonSettings: {
          method: ComparisonMethod.SSIM,
          threshold: 0.9,
        },
        errorValue: 1.5,
      },
      { isEditable: { canEdit: true }, isEditing: true }
    );

    fireEvent.click(rendered.getByText("Cancel"));

    expect(dispatch).toBeCalledWith({ type: ActionType.CANCEL });
  });

  it("should dispatch error value when pressing the match button", () => {
    const { rendered, dispatch } = setup(
      {
        comparisonSettings: {
          method: ComparisonMethod.SSIM,
          threshold: 0.9,
        },
        errorValue: 1.5,
      },
      { isEditable: { canEdit: true }, isEditing: true }
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
        comparisonSettings: {
          method: ComparisonMethod.SSIM,
          threshold: 0.9,
        },
        errorValue: 1.5,
      },
      {
        isEditable: { canEdit: true },
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
