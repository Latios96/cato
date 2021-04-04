import React from "react";

import { ProjectsViewStateless } from "./ProjectsView";
import { Meta } from "@storybook/react";
import { HashRouter } from "react-router-dom";

export default {
  title: "ProjectsView",
  component: ProjectsViewStateless,
} as Meta;

export const Loading: React.VFC<{}> = () => (
  <ProjectsViewStateless
    fetchResult={{ isLoading: true, data: undefined, error: undefined }}
  />
);
export const Error: React.VFC<{}> = () => (
  <ProjectsViewStateless
    fetchResult={{
      isLoading: false,
      data: undefined,
      error: "This is an error message",
    }}
  />
);
export const NoProjects: React.VFC<{}> = () => (
  <ProjectsViewStateless
    fetchResult={{ isLoading: false, data: [], error: undefined }}
  />
);
export const WithProjects: React.VFC<{}> = () => (
  <HashRouter>
    <ProjectsViewStateless
      fetchResult={{
        isLoading: false,
        data: [
          { id: 1, name: "test 1" },
          { id: 2, name: "test 2" },
        ],
        error: undefined,
      }}
    />
  </HashRouter>
);
