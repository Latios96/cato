import React from "react";
import { Card } from "react-bootstrap";
import Project from "../../models/Project";
import styles from "./ProjectComponent.module.css";

interface Props {
  project: Project;
}

function ProjectComponent(props: Props) {
  return (
    <Card style={{ width: "18rem" }}>
      <Card.Body>
        <Card.Title>{props.project.name}</Card.Title>
      </Card.Body>
    </Card>
  );
}

export default ProjectComponent;
