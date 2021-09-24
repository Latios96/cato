import React, { useCallback, useEffect, useReducer } from "react";
import { ComparisonSettingsDto, TestResultDto } from "../../catoapimodels";
import axios from "axios";
import { ActionType, getInitialState, reducer } from "./reducer";
import TestResultComparisonResultImpl from "./TestResultComparisonResultImpl";

interface Props {
  testResult: TestResultDto;
}

function TestResultComparisonResult(props: Props) {
  const [state, dispatch] = useReducer(
    reducer,
    getInitialState(props.testResult)
  );

  const checkIsEditable = useCallback(() => {
    dispatch({ type: ActionType.CHECK_IS_EDITABLE });
    axios
      .get(
        `/api/v1/test_edits/can-edit/${props.testResult.id}/comparison_settings`
      )
      .then((result) => {
        dispatch({ type: ActionType.SET_IS_EDITABLE, payload: result.data });
      })
      .catch(() => {
        dispatch({
          type: ActionType.SET_IS_EDITABLE,
          payload: { can_edit: false },
        });
      });
  }, [props.testResult.id]);

  useEffect(() => {
    dispatch({
      type: ActionType.RESET,
      payload: getInitialState(props.testResult),
    });
    checkIsEditable();
  }, [
    dispatch,
    props.testResult,
    checkIsEditable,
    props.testResult.comparison_settings,
  ]);

  const updateComparisonSettings = (
    comparisonSettings: ComparisonSettingsDto
  ) => {
    dispatch({ type: ActionType.UPDATING_START });
    axios
      .post("/api/v1/test_edits/comparison_settings", {
        test_result_id: props.testResult.id,
        new_value: comparisonSettings,
      })
      .then(() => {
        dispatch({ type: ActionType.UPDATING_END });
      });
  };
  return (
    <TestResultComparisonResultImpl
      state={state}
      dispatch={dispatch}
      testResult={props.testResult}
      updateComparisonSettings={updateComparisonSettings}
    />
  );
}

export default TestResultComparisonResult;
