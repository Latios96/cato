import RunListImplementation from "./RunListImplementation";
import React from "react";
import { render } from "@testing-library/react";
import { Page } from "../../../components/Pagination/Page";
import { RunDto, RunStatusDto } from "../../../catoapimodels";
import { HashRouter } from "react-router-dom";

describe("RunListImplementation", () => {
  it("should display a loading skeletion while loading", () => {
    const rendered = render(
      <RunListImplementation
        projectId={1}
        runs={undefined}
        isLoading={true}
        error={undefined}
      />
    );
    expect(
      rendered.container.getElementsByClassName("react-loading-skeleton").length
    ).toBeGreaterThan(1);
  });

  it("should display an error message if there is an error", () => {
    const rendered = render(
      <RunListImplementation
        projectId={1}
        runs={undefined}
        isLoading={false}
        error={new Error("My error message")}
      />
    );

    expect(rendered.getByText("My error message")).toBeInTheDocument();
  });

  it("should display a list of runs", () => {
    const page: Page<RunDto> = {
      page_number: 1,
      page_size: 3,
      total_entity_count: 3,
      entities: [
        {
          id: 1,
          project_id: 2,
          started_at: "2021-08-05T19:10:52.815332",
          status: RunStatusDto.SUCCESS,
        },
        {
          id: 2,
          project_id: 2,
          started_at: "2021-08-05T19:10:52.815332",
          status: RunStatusDto.SUCCESS,
        },
        {
          id: 3,
          project_id: 2,
          started_at: "2021-08-05T19:10:52.815332",
          status: RunStatusDto.SUCCESS,
        },
      ],
    };
    const rendered = render(
      <HashRouter>
        <RunListImplementation
          projectId={1}
          runs={page}
          isLoading={false}
          error={undefined}
        />
      </HashRouter>
    );

    expect(rendered.getByText("Run #1")).toBeInTheDocument();
    expect(rendered.getByText("Run #2")).toBeInTheDocument();
    expect(rendered.getByText("Run #3")).toBeInTheDocument();
  });
});
