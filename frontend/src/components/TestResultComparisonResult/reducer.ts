import { TestResultDtoComparisonPick } from "./TestResultComparisonResultImpl";
import {
  CanBeEdited,
  ComparisonMethod,
  ComparisonSettings,
} from "../../catoapimodels/catoapimodels";

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
function getInitialThreshold(comparison_settings?: ComparisonSettings) {
  if (comparison_settings) {
    return comparison_settings.threshold.toFixed(3);
  }
  return "0.8";
}

function getInitialMethod(comparison_settings?: ComparisonSettings) {
  return comparison_settings?.method || ComparisonMethod.SSIM;
}

export function getInitialState(
  testResult: TestResultDtoComparisonPick
): State {
  return {
    isEditing: false,
    isUpdating: false,
    isEditableChecking: true,
    isEditable: { canEdit: false, message: "" },
    currentThreshold: getInitialThreshold(testResult.comparisonSettings),
    currentMethod: getInitialMethod(testResult.comparisonSettings),
    originalThreshold: getInitialThreshold(testResult.comparisonSettings),
    originalMethod: getInitialMethod(testResult.comparisonSettings),
  };
}
