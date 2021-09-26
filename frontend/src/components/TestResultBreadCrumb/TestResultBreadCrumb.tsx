import React from "react";
import { Breadcrumb } from "react-bootstrap";
import CopyToClipboardButton from "../CopyToClipboardButton/CopyToClipboardButton";

interface Props {
  projectId: number;
  runId: number;
  suiteId: number;
  suiteName: string;
  testName?: string;
}

const TestResultBreadCrumb = (props: Props) => {
  return (
    <div>
      <Breadcrumb>
        <Breadcrumb.Item
          href={`#/projects/${props.projectId}/runs/${props.runId}`}
        >
          Run {`#${props.runId}`}
        </Breadcrumb.Item>
        <Breadcrumb.Item
          href={`#/projects/${props.projectId}/runs/${props.runId}/suites/${props.suiteId}`}
        >
          {props.suiteName}
        </Breadcrumb.Item>
        {props.testName ? (
          <>
            <Breadcrumb.Item>{props.testName}</Breadcrumb.Item>
            <div style={{ marginLeft: "auto" }}>
              <CopyToClipboardButton
                tooltipText={"Copy test identifier"}
                clipboardText={`${props.suiteName}/${props.testName}`}
                copiedMessage={"Copied test identifier to clipboard"}
              />
            </div>
          </>
        ) : (
          <React.Fragment />
        )}
      </Breadcrumb>
    </div>
  );
};

export default TestResultBreadCrumb;
