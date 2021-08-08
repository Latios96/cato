import React, { Component, FunctionComponent, ReactNode } from "react";
import _ from "lodash";

export class LoadingState extends Component {
  render() {
    return this.props.children;
  }
}

export class ErrorState extends Component {
  render() {
    return this.props.children;
  }
}

export class DataLoadedState extends Component {
  render() {
    return this.props.children;
  }
}

interface Props {
  isLoading: boolean;
  error?: Error;
}

export const LoadingStateHandler: FunctionComponent<Props> = (props) => {
  const getTypeOfChild = (child: any) => {
    return _.get(child, "type");
  };
  const getChildOfType = (type: any): ReactNode | undefined => {
    if (
      !Array.isArray(props.children) &&
      getTypeOfChild(props.children) === type
    ) {
      return props.children;
    }
    if (Array.isArray(props.children)) {
      return props.children.find((child) => getTypeOfChild(child) === type);
    }
  };
  const loadingState = getChildOfType(LoadingState);
  const errorState = getChildOfType(ErrorState);
  const dataLoaded = getChildOfType(DataLoadedState);
  if (props.isLoading && loadingState) {
    return <>{loadingState}</> || null;
  } else if (props.error && errorState) {
    return <>{errorState}</> || null;
  } else if (!props.isLoading && dataLoaded) {
    return <>{dataLoaded}</> || null;
  } else {
    return <></>;
  }
};
