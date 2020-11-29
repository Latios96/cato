import React, { Component } from "react";
interface Props {
  projectId: number;
}
interface State {}
class ProjectRunsView extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {};
  }
  render() {
    return <div>{this.props.projectId}</div>;
  }
}

export default ProjectRunsView;
