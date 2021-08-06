import React, { Component, FunctionComponent } from "react";
import _ from "lodash";
import { instance } from "@storybook/node-logger";

export class LoadingState extends Component {
  render() {
    return <div>LOADING</div>;
  }
}

export class ErrorState extends Component {
  render() {
    return <div>ErrorState</div>;
  }
}

export class DataLoaded extends Component {
  render() {
    return <div>DataLoaded</div>;
  }
}

interface Props {
  isLoading: boolean;
  data: any;
  error?: Error;
}

export const LoadingStateHandler: FunctionComponent<Props> = (props) => {
  const getTypeOfChild = (child: any) => {
    return _.get(child, "type");
  };
  const getChildOfType = (type: any) => {
    if (
      +!Array.isArray(props.children) &&
      getTypeOfChild(props.children) === DataLoaded
    ) {
      return props.children;
    }
  };
  const loadingState = getChildOfType(LoadingState);
  if (props.isLoading && loadingState) {
    return;
  }
};
