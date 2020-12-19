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
import AboutPage from "../../pages/AboutPage";

interface ProjectPageMatchParams {
  projectId: string;
  runId: string;
  currentTab: string;
}

interface ProjectPageMatchProps
  extends RouteComponentProps<ProjectPageMatchParams> {}

function App() {
  return (
    <HashRouter>
      <Switch>
        <Route exact path="/" component={() => <ProjectsPage />} />
        <Route exact path="/about" component={() => <AboutPage />} />
        <Route
          exact
          path="/projects/:projectId/runs/:runId?/:currentTab?"
          component={(props: ProjectPageMatchProps) => {
            return (
              <ProjectPage
                projectId={parseInt(props.match.params.projectId)}
                currentRunId={
                  props.match.params.runId != null
                    ? parseInt(props.match.params.runId)
                    : null
                }
                currentTab={props.match.params.currentTab}
              />
            );
          }}
        />
      </Switch>
    </HashRouter>
  );
}

export default App;
