import React, { useCallback, useContext, useEffect, useReducer } from "react";
import axios from "axios";
import { ActionType, getInitialState, reducer } from "./reducer";
import { TestResultComparisonResultImpl } from "./TestResultComparisonResultImpl";
import { TestResultUpdateContext } from "../TestResultUpdateContext/TestResultUpdateContext";
import {
  ComparisonSettings,
  TestResultDto,
} from "../../catoapimodels/catoapimodels";

interface Props {
  testResult: TestResultDto;
}

function TestResultComparisonResult(props: Props) {
  const [state, dispatch] = useReducer(
    reducer,
    getInitialState(props.testResult)
  );
  const { update } = useContext(TestResultUpdateContext);

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
          payload: { canEdit: false },
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
    props.testResult.comparisonSettings,
  ]);

  const updateComparisonSettings = (comparisonSettings: ComparisonSettings) => {
    dispatch({ type: ActionType.UPDATING_START });
    axios
      .post("/api/v1/test_edits/comparison_settings", {
        testResultId: props.testResult.id,
        newValue: comparisonSettings,
      })
      .then(() => {
        dispatch({ type: ActionType.UPDATING_END });
        update(props.testResult.id);
      })
      .catch(() => {
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
