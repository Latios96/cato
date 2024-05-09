import { ProjectsViewPresenter } from "./ProjectsView";
import { render } from "@testing-library/react";
import { HashRouter } from "react-router-dom";
import React from "react";
import { ProjectStatus } from "../../../../catoapimodels/catoapimodels";

const isError = {
  isLoading: false,
  data: undefined,
  error: new Error("This is an error message"),
};
const noProjects = { isLoading: false, data: [], error: undefined };
const withProjects = {
  isLoading: false,
  data: [
    { id: 1, name: "test 1", status: ProjectStatus.ARCHIVED },
    { id: 2, name: "test 2", status: ProjectStatus.ARCHIVED },
  ],
  error: undefined,
};
describe("ProjectsView", () => {
  it("should display a error message", () => {
    const rendered = render(<ProjectsViewPresenter fetchResult={isError} />);

    expect(rendered.getByText("This is an error message")).toBeInTheDocument();
  });

  it("should display a placeholder text", () => {
    const rendered = render(<ProjectsViewPresenter fetchResult={noProjects} />);

    expect(rendered.getByText("No projects found")).toBeInTheDocument();
  });

  it("should display a project list", () => {
    const rendered = render(
      <HashRouter>
        <ProjectsViewPresenter fetchResult={withProjects} />
      </HashRouter>
    );

    expect(rendered.getByText("test 1")).toBeInTheDocument();
    expect(rendered.getByText("test 2")).toBeInTheDocument();
  });
});
