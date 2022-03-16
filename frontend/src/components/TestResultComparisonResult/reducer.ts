import {
  ComparisonMethodDto,
  ComparisonSettingsDto,
} from "../../catoapimodels";
import { TestResultDtoComparisonPick } from "./TestResultComparisonResultImpl";
import { CanBeEdited } from "../../catoapimodels/catoapimodels";

export interface State {
  isEditing: boolean;
  isUpdating: boolean;
  isEditableChecking: boolean;
  isEditable: CanBeEdited;
  currentThreshold: string;
  currentMethod: string;
  originalThreshold: string;
  originalMethod: string;
}

export enum ActionType {
  CHECK_IS_EDITABLE = "CHECK_IS_EDITABLE",
  SET_IS_EDITABLE = "SET_IS_EDITABLE",
  START_EDITING = "START_EDITING",
  CANCEL = "CANCEL",
  SET_CURRENT_METHOD = "SET_CURRENT_METHOD",
  SET_CURRENT_THRESHOLD = "SET_CURRENT_THRESHOLD",
  UPDATING_START = "UPDATING_START",
  UPDATING_END = "UPDATING_END",
  RESET = "RESET",
}

export interface Action {
  type: ActionType;
  payload?: any;
}

export function reducer(state: State, action: Action) {
  switch (action.type) {
    case ActionType.CHECK_IS_EDITABLE:
      return { ...state, isEditableChecking: true };
    case ActionType.SET_IS_EDITABLE:
      return {
        ...state,
        isEditableChecking: false,
        isEditable: action.payload,
      };
    case ActionType.START_EDITING:
      return {
        ...state,
        isEditing: true,
      };
    case ActionType.CANCEL:
      return {
        ...state,
        isEditing: false,
        currentMethod: state.originalMethod,
        currentThreshold: state.originalThreshold,
      };
    case ActionType.SET_CURRENT_METHOD:
      return {
        ...state,
        currentMethod: action.payload,
      };
    case ActionType.SET_CURRENT_THRESHOLD:
      return {
        ...state,
        currentThreshold: action.payload,
      };
    case ActionType.UPDATING_END:
      return {
        ...state,
        isUpdating: false,
      };
    case ActionType.UPDATING_START:
      return {
        ...state,
        isUpdating: true,
        isEditing: false,
      };
    case ActionType.RESET:
      return action.payload;
    default:
      throw new Error();
  }
}
function getInitialThreshold(
  comparison_settings?: ComparisonSettingsDto | null
) {
  if (comparison_settings && comparison_settings.threshold !== "NaN") {
    return comparison_settings.threshold.toFixed(3);
  }
  return "0.8";
}

function getInitialMethod(comparison_settings?: ComparisonSettingsDto | null) {
  return comparison_settings?.method || ComparisonMethodDto.SSIM;
}

export function getInitialState(
  testResult: TestResultDtoComparisonPick
): State {
  return {
    isEditing: false,
    isUpdating: false,
    isEditableChecking: true,
    isEditable: { can_edit: false, message: "" },
    currentThreshold: getInitialThreshold(testResult.comparison_settings),
    currentMethod: getInitialMethod(testResult.comparison_settings),
    originalThreshold: getInitialThreshold(testResult.comparison_settings),
    originalMethod: getInitialMethod(testResult.comparison_settings),
  };
}
