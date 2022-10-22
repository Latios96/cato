import { fireEvent, render } from "@testing-library/react";
import RunBatchListEntry from "./RunBatchListEntry";
import { HashRouter } from "react-router-dom";
import {
  RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS,
  RUN_BATCH_AGGREGATE_WITH_SINGLE_RUN,
} from "./RunBatchTestData";

describe("RunBatchListEntry", () => {
  it("should render run batch collapsed by default", () => {
    const rendered = render(
      <RunBatchListEntry
        projectId={1}
        runBatch={RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS}
      />
    );

    expect(
      rendered.queryByRole("button", { expanded: true })
    ).not.toBeInTheDocument();
  });

  it("should render run name for run batch with multiple runs", () => {
    const rendered = render(
      <RunBatchListEntry
        projectId={1}
        runBatch={RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS}
      />
    );

    expect(rendered.getByText("build")).toBeInTheDocument();
  });

  it("should render run id for run batch with single run", () => {
    const rendered = render(
      <HashRouter>
        <RunBatchListEntry
          projectId={1}
          runBatch={RUN_BATCH_AGGREGATE_WITH_SINGLE_RUN}
        />
      </HashRouter>
    );

    expect(rendered.getByText("#249")).toBeInTheDocument();
  });

  it("should render run batch and all runs in batch", () => {
    const rendered = render(
      <HashRouter>
        <RunBatchListEntry
          projectId={1}
          runBatch={RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS}
        />
      </HashRouter>
    );

    expect(rendered.queryByText("#257")).not.toBeInTheDocument();
    fireEvent.click(rendered.getByRole("button", { expanded: false }));

    expect(rendered.getByText("#257")).toBeInTheDocument();
    expect(rendered.getByText("#258")).toBeInTheDocument();
    expect(rendered.getByText("#259")).toBeInTheDocument();
  });
});
