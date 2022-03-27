import React from "react";
import "./App.css";
import {
  Switch,
  Route,
  RouteComponentProps,
  BrowserRouter,
} from "react-router-dom";
import ProjectsPage from "../../pages/ProjectsPage";
import ProjectPage from "../../pages/ProjectPage/ProjectPage";
import AboutPage from "../../pages/AboutPage";
import { QueryClient, QueryClientProvider } from "react-query";
import RunOverviewPage from "../../pages/RunPages/RunOverviewPage";
import RunSuitePage from "../../pages/RunPages/RunSuitesPage";
import RunTestsPage from "../../pages/RunPages/RunTestsPage";
import { AuthenticatedUserProvider } from "../../contexts/AuthenticatedUserContext/AuthenticatedUserContext";
import { UserProvider } from "../../contexts/AuthenticatedUserContext/UserContext";
import RenderOnAnonymous from "../Authentication/RenderOnAnonymous";
import LoginPage from "../../pages/LoginPage/LoginPage";
import RenderOnAuthenticated from "../Authentication/RenderOnAuthenticated";
import RenderPlaceholderWhileUserLoading from "../Authentication/RenderPlaceholderWhileUserLoading";

interface ProjectPageMatchParams {
  projectId: string;
  runId: string;
}

interface ProjectPageMatchProps
  extends RouteComponentProps<ProjectPageMatchParams> {}

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <UserProvider>
        <RenderPlaceholderWhileUserLoading
          renderWhenLoaded={() => {
            return (
              <AuthenticatedUserProvider>
                <RenderOnAnonymous render={() => <LoginPage />} />
                <RenderOnAuthenticated
                  render={() => {
                    return (
                      <BrowserRouter>
                        <Switch>
                          <Route
                            exact
                            path="/"
                            component={() => <ProjectsPage />}
                          />
                          <Route
                            exact
                            path="/about"
                            component={() => <AboutPage />}
                          />
                          <Route
                            exact
                            path="/projects/:projectId"
                            component={(props: ProjectPageMatchProps) => {
                              return (
                                <ProjectPage
                                  projectId={parseInt(
                                    props.match.params.projectId
                                  )}
                                />
                              );
                            }}
                          />
                          <Route
                            exact
                            path="/projects/:projectId/runs/:runId"
                            component={(props: ProjectPageMatchProps) => {
                              return (
                                <RunOverviewPage
                                  projectId={parseInt(
                                    props.match.params.projectId
                                  )}
                                  runId={parseInt(props.match.params.runId)}
                                />
                              );
                            }}
                          />
                          <Route
                            exact
                            path="/projects/:projectId/runs/:runId/suites"
                            component={(props: ProjectPageMatchProps) => {
                              return (
                                <RunSuitePage
                                  projectId={parseInt(
                                    props.match.params.projectId
                                  )}
                                  runId={parseInt(props.match.params.runId)}
                                />
                              );
                            }}
                          />
                          <Route
                            exact
                            path="/projects/:projectId/runs/:runId/tests"
                            component={(props: ProjectPageMatchProps) => {
                              return (
                                <RunTestsPage
                                  projectId={parseInt(
                                    props.match.params.projectId
                                  )}
                                  runId={parseInt(props.match.params.runId)}
                                />
                              );
                            }}
                          />
                        </Switch>
                      </BrowserRouter>
                    );
                  }}
                />
              </AuthenticatedUserProvider>
            );
          }}
        />
      </UserProvider>
    </QueryClientProvider>
  );
}

export default App;
