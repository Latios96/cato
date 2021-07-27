import React from "react";
import { Breadcrumb, Button } from "react-bootstrap";
import { Clipboard } from "react-bootstrap-icons";
import styles from "../ImageComparison/ImageComparison.module.scss";

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
            <Button
              className={styles.buttonNoShadowOnFocus}
              onClick={() => {
                navigator.clipboard.writeText(
                  `${props.suiteName}/${props.testName}`
                );
              }}
              variant={"link"}
              style={{ marginLeft: "auto", padding: "0px" }}
              title={"Copy test identifier to clipboard"}
            >
              <Clipboard size={16} />
            </Button>
          </>
        ) : (
          <React.Fragment />
        )}
      </Breadcrumb>
    </div>
  );
};

export default TestResultBreadCrumb;
