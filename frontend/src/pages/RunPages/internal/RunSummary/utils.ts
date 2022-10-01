import { RunAggregate } from "../../../../catoapimodels/catoapimodels";

export interface StatusPercentage {
  waitingToStart: number;
  running: number;
  succeeded: number;
  failed: number;
}
export function calculateStatusPercentage(
  runAggregate: Pick<RunAggregate, "testCount" | "progress">
): StatusPercentage {
  return {
    waitingToStart:
      (runAggregate.progress.waitingTestCount / runAggregate.testCount) * 100,
    running:
      (runAggregate.progress.runningTestCount / runAggregate.testCount) * 100,
    succeeded:
      (runAggregate.progress.succeededTestCount / runAggregate.testCount) * 100,
    failed:
      (runAggregate.progress.failedTestCount / runAggregate.testCount) * 100,
  };
}
