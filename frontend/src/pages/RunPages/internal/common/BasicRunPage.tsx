import React, { PropsWithChildren } from "react";
import BasicPage from "../../../BasicPage";
import SideBar from "./SideBar";
import { CurrentPage, toDisplayString } from "./CurrentPage";

interface Props {
  projectId: number;
  runId: number;
  currentPage: CurrentPage;
}

const BasicRunPage = (props: PropsWithChildren<Props>) => {
  return (
    <BasicPage
      title={`Run #${props.runId} · ${toDisplayString(props.currentPage)}`}
    >
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
