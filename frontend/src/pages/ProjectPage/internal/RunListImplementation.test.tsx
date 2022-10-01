import RunListImplementation from "./RunListImplementation";
import React from "react";
import { render } from "@testing-library/react";
import { Page } from "../../../components/Pagination/Page";
import { HashRouter } from "react-router-dom";
import {
  OS,
  RunBatchProvider,
  RunAggregate,
  RunStatus,
} from "../../../catoapimodels/catoapimodels";

describe("RunListImplementation", () => {
  it("should display a loading skeletion while loading", () => {
    const rendered = render(
      <RunListImplementation
        projectId={1}
        runs={undefined}
        isLoading={true}
        error={undefined}
        branches={[]}
        selectedBranches={new Set()}
        pageChanged={jest.fn()}
        filteredBranchesChanged={jest.fn()}
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
        branches={[]}
        selectedBranches={new Set()}
        pageChanged={jest.fn()}
        filteredBranchesChanged={jest.fn()}
      />
    );

    expect(rendered.getByText("My error message")).toBeInTheDocument();
  });

  it("should display a list of runs", () => {
    const page: Page<RunAggregate> = {
      pageNumber: 1,
      pageSize: 3,
      totalEntityCount: 3,
      entities: [
        {
          id: 1,
          projectId: 2,
          startedAt: "2021-08-05T19:10:52.815332",
          status: RunStatus.SUCCESS,
          duration: 1,
          branchName: "default",
          runInformation: {
            id: 0,
            runId: 0,
            os: OS.WINDOWS,
            computerName: "cray",
            localUsername: "username",
            runInformationType: RunBatchProvider.LOCAL_COMPUTER,
          },
          suiteCount: 1,
          testCount: 1,
          progress: {
            progressPercentage: 0,
            waitingTestCount: 2,
            runningTestCount: 3,
            failedTestCount: 4,
            succeededTestCount: 1,
          },
        },
        {
          id: 2,
          projectId: 2,
          startedAt: "2021-08-05T19:10:52.815332",
          status: RunStatus.SUCCESS,
          duration: 1,
          branchName: "default",
          runInformation: {
            id: 0,
            runId: 0,
            os: OS.WINDOWS,
            computerName: "cray",
            localUsername: "username",
            runInformationType: RunBatchProvider.LOCAL_COMPUTER,
          },
          suiteCount: 1,
          testCount: 1,
          progress: {
            progressPercentage: 0,
            waitingTestCount: 2,
            runningTestCount: 3,
            failedTestCount: 4,
            succeededTestCount: 1,
          },
        },
        {
          id: 3,
          projectId: 2,
          startedAt: "2021-08-05T19:10:52.815332",
          status: RunStatus.SUCCESS,
          duration: 1,
          branchName: "default",
          runInformation: {
            id: 0,
            runId: 0,
            os: OS.WINDOWS,
            computerName: "cray",
            localUsername: "username",
            runInformationType: RunBatchProvider.LOCAL_COMPUTER,
          },
          suiteCount: 1,
          testCount: 1,
          progress: {
            progressPercentage: 0,
            waitingTestCount: 2,
            runningTestCount: 3,
            failedTestCount: 4,
            succeededTestCount: 1,
          },
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
          branches={[]}
          selectedBranches={new Set()}
          pageChanged={jest.fn()}
          filteredBranchesChanged={jest.fn()}
        />
      </HashRouter>
    );

    expect(rendered.getByText("Run #1")).toBeInTheDocument();
    expect(rendered.getByText("Run #2")).toBeInTheDocument();
    expect(rendered.getByText("Run #3")).toBeInTheDocument();
  });
});
