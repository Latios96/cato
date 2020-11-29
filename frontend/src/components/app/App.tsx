import React from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  RouteComponentProps,
} from "react-router-dom";
import ProjectsPage from "../../pages/ProjectsPage";
import ProjectPage from "../../pages/ProjectPage";

interface MatchParams {
  projectId: string;
}

interface MatchProps extends RouteComponentProps<MatchParams> {}

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={() => <ProjectsPage />} />
        <Route
          exact
          path="/projects/:projectId"
          component={(props: MatchProps) => {
            return (
              <ProjectPage projectId={parseInt(props.match.params.projectId)} />
            );
          }}
        />
      </Switch>
    </Router>
  );
}

export default App;
