import { useHistory } from "react-router-dom";
import { Tab, Tabs } from "react-bootstrap";
import React, { useEffect, useState } from "react";

interface Props {
  projectId: number;
  runId: number;
  currentTab: string;
}

export default function RunSummaryTabComponent(props: Props) {
  const [currentTab, setCurrentTab] = useState(props.currentTab);
  let history = useHistory();
  useEffect(() => {
    setCurrentTab(props.currentTab);
  }, [props.currentTab]);
  return (
    <Tabs
      id="controlled-tab-example"
      activeKey={currentTab}
      onSelect={(k) =>
        history.push(`/projects/${props.projectId}/runs/${props.runId}/${k}`)
      }
    >
      <Tab eventKey="suites" title="Suites">
        Suites
      </Tab>
      <Tab eventKey="tests" title="Tests">
        Tests
      </Tab>
    </Tabs>
  );
}
