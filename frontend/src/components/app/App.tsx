import React from "react";
import "./App.css";
import {
  Switch,
  Route,
  RouteComponentProps,
  HashRouter,
} from "react-router-dom";
import ProjectsPage from "../../pages/ProjectsPage";
import ProjectPage from "../../pages/ProjectPage";

interface ProjectPageMatchParams {
  projectId: string;
  runId: string;
}

interface ProjectPageMatchProps
  extends RouteComponentProps<ProjectPageMatchParams> {}

function App() {
  return (
    <HashRouter>
      <Switch>
        <Route exact path="/" component={() => <ProjectsPage />} />
        <Route
          exact
          path="/projects/:projectId/runs/:runId?"
          component={(props: ProjectPageMatchProps) => {
            return (
              <ProjectPage
                projectId={parseInt(props.match.params.projectId)}
                currentRunId={
                  props.match.params.runId != null
                    ? parseInt(props.match.params.runId)
                    : null
                }
              />
            );
          }}
        />
      </Switch>
    </HashRouter>
  );
}

export default App;
