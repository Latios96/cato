import React, { Component } from "react";
import SuiteResult from "../../models/SuiteResult";
interface Props {
  suiteResult: SuiteResult;
}
interface State {}
class SuiteResultComponent extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
  }
  render() {
    return <div>{this.props.suiteResult.suite_name}</div>;
  }
}

export default SuiteResultComponent;
