import { ProjectsViewStateless } from "./ProjectsView";
import { render } from "@testing-library/react";
import { HashRouter } from "react-router-dom";
import React from "react";

const isLoading = { isLoading: true, data: undefined, error: undefined };
const isError = {
  isLoading: false,
  data: undefined,
  error: "This is an error message",
};
const noProjects = { isLoading: false, data: [], error: undefined };
const withProjects = {
  isLoading: false,
  data: [
    { id: 1, name: "test 1" },
    { id: 2, name: "test 2" },
  ],
  error: undefined,
};
describe("ProjectsView", () => {
  it("should display a loading indicator while loading", () => {
    const rendered = render(<ProjectsViewStateless fetchResult={isLoading} />);

    expect(rendered.getByRole("LoadingIndicator")).toBeInTheDocument();
  });

  it("should display a error message", () => {
    const rendered = render(<ProjectsViewStateless fetchResult={isError} />);

    expect(rendered.getByText("This is an error message")).toBeInTheDocument();
  });

  it("should display a placeholder text", () => {
    const rendered = render(<ProjectsViewStateless fetchResult={noProjects} />);

    expect(rendered.getByText("No projects found")).toBeInTheDocument();
  });

  it("should display a project list", () => {
    const rendered = render(
      <HashRouter>
        <ProjectsViewStateless fetchResult={withProjects} />
      </HashRouter>
    );

    expect(rendered.getByText("test 1")).toBeInTheDocument();
    expect(rendered.getByText("test 2")).toBeInTheDocument();
  });
});
