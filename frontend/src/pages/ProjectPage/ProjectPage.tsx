import React from "react";
import BasicPage from "../BasicPage";
import RunList from "./internal/RunList/RunList";
import ProjectInformation from "./internal/ProjectInformation";
import { Form } from "react-bootstrap";
import { useToggle } from "rooks";
import RunBatchList from "./internal/RunBatchList/RunBatchList";

interface Props {
  projectId: number;
}

function ProjectPage(props: Props) {
  const [useRunBatches, toggle] = useToggle(false);

  return (
    <BasicPage>
      <ProjectInformation projectId={props.projectId} />
      <div
        className={"ml-auto mr-auto "}
        style={{ width: "850px", marginTop: "35px" }}
      >
        <Form>
          <Form.Check
            type="switch"
            id="custom-switch"
            label="Use Run Batches"
            onChange={(e) => toggle(e.target.value)}
          />
        </Form>
      </div>
      {useRunBatches ? (
        <RunBatchList projectId={props.projectId} />
      ) : (
        <RunList projectId={props.projectId} />
      )}
    </BasicPage>
  );
}

export default ProjectPage;
