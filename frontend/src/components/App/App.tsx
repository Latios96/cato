import React from "react";
import "./App.css";
import {
  Switch,
  Route,
  RouteComponentProps,
  HashRouter,
} from "react-router-dom";
import ProjectsPage from "../../pages/ProjectsPage";
import ProjectPage from "../../pages/ProjectPage/ProjectPage";
import AboutPage from "../../pages/AboutPage";
import { QueryClient, QueryClientProvider } from "react-query";

interface ProjectPageMatchParams {
  projectId: string;
  runId: string;
  currentTab: string;
  suiteOrTestId: string;
}

interface ProjectPageMatchProps
  extends RouteComponentProps<ProjectPageMatchParams> {}

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <HashRouter>
        <Switch>
          <Route exact path="/" component={() => <ProjectsPage />} />
          <Route exact path="/about" component={() => <AboutPage />} />
          <Route
            exact
            path="/projects/:projectId"
            component={(props: ProjectPageMatchProps) => {
              return (
                <ProjectPage
                  projectId={parseInt(props.match.params.projectId)}
                />
              );
            }}
          />
        </Switch>
      </HashRouter>
    </QueryClientProvider>
  );
}

export default App;
