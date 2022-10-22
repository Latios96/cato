import { render } from "@testing-library/react";
import {
  RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS,
  RUN_BATCH_AGGREGATE_WITH_SINGLE_RUN,
} from "./RunBatchTestData";
import RunBatchListRow from "./RunBatchListRow";

describe("RunBatchListRow", () => {
  describe("rendering of Expander", () => {
    it("should render expander if RunBatch is expandable", () => {
      const rendered = render(
        <RunBatchListRow
          isIndented={false}
          isExpandable={true}
          representsSingleRun={false}
          label={<></>}
          runLike={{
            ...RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS,
            ...RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS.runs[0],
          }}
          isExpanded={false}
          onExpandToggleClick={jest.fn}
        />
      );

      expect(
        rendered.getByRole("button", { expanded: false })
      ).toBeInTheDocument();
    });

    it("should not render expander if Runbatch is not expandable", () => {
      const rendered = render(
        <RunBatchListRow
          isIndented={false}
          isExpandable={false}
          representsSingleRun={true}
          label={<></>}
          runLike={{
            ...RUN_BATCH_AGGREGATE_WITH_SINGLE_RUN,
            ...RUN_BATCH_AGGREGATE_WITH_SINGLE_RUN.runs[0],
          }}
          isExpanded={false}
          onExpandToggleClick={jest.fn}
        />
      );

      expect(
        rendered.queryByRole("button", { expanded: false })
      ).not.toBeInTheDocument();
    });
  });

  describe("rendering of RunBatchProviderInformation", () => {
    it("should render RunBatchProviderInformation if RunBatch has single run", () => {
      const rendered = render(
        <RunBatchListRow
          isIndented={false}
          isExpandable={false}
          representsSingleRun={true}
          label={<></>}
          runLike={{
            ...RUN_BATCH_AGGREGATE_WITH_SINGLE_RUN,
            ...RUN_BATCH_AGGREGATE_WITH_SINGLE_RUN.runs[0],
          }}
          isExpanded={false}
          onExpandToggleClick={jest.fn}
        />
      );

      expect(rendered.getByTitle("Github Actions")).toBeInTheDocument();
    });

    it("should render RunBatchProviderInformation if RunBatch has multiple runs", () => {
      const rendered = render(
        <RunBatchListRow
          isIndented={false}
          isExpandable={true}
          representsSingleRun={false}
          label={<></>}
          runLike={{
            ...RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS,
            ...RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS.runs[0],
          }}
          isExpanded={false}
          onExpandToggleClick={jest.fn}
        />
      );

      expect(rendered.getByTitle("Github Actions")).toBeInTheDocument();
    });

    it("should not render RunBatchProviderInformation if not a single run or is not expandable (e.g. is indented)", () => {
      const rendered = render(
        <RunBatchListRow
          isIndented={true}
          isExpandable={false}
          representsSingleRun={false}
          label={<></>}
          runLike={RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS.runs[0]}
          isExpanded={false}
          onExpandToggleClick={jest.fn}
        />
      );

      expect(rendered.queryByTitle("Github Actions")).not.toBeInTheDocument();
    });
  });

  describe("rendering of RunInformation", () => {
    it("should render RunInformation if single run and not expandable", () => {
      const rendered = render(
        <RunBatchListRow
          isIndented={false}
          isExpandable={false}
          representsSingleRun={true}
          label={<></>}
          runLike={{
            ...RUN_BATCH_AGGREGATE_WITH_SINGLE_RUN,
            ...RUN_BATCH_AGGREGATE_WITH_SINGLE_RUN.runs[0],
          }}
          isExpanded={false}
          onExpandToggleClick={jest.fn}
        />
      );

      expect(rendered.getByTitle("OS is unknown")).toBeInTheDocument();
    });
    it("should not render RunInformation if not single run", () => {
      const rendered = render(
        <RunBatchListRow
          isIndented={false}
          isExpandable={true}
          representsSingleRun={false}
          label={<></>}
          runLike={{
            ...RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS,
            ...RUN_BATCH_AGGREGATE_WITH_MULTIPLE_RUNS.runs[0],
          }}
          isExpanded={false}
          onExpandToggleClick={jest.fn}
        />
      );

      expect(rendered.queryByTitle("OS is unknown")).not.toBeInTheDocument();
    });
  });
});
