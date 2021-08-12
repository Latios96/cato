import React from "react";
import BasicPage from "../../../BasicPage";
import SideBar from "./SideBar";
import { CurrentPage } from "./CurrentPage";

interface Props {
  projectId: number;
  runId: number;
  currentPage: CurrentPage;
}

const BasicRunPage: React.FunctionComponent<Props> = (props) => {
  return (
    <BasicPage>
      <div style={{ display: "flex" }}>
        <SideBar
          projectId={props.projectId}
          runId={props.runId}
          currentPage={props.currentPage}
        />
        {props.children}
      </div>
    </BasicPage>
  );
};

export default BasicRunPage;
