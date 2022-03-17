import { RunSummaryDto } from "../../../../catoapimodels/catoapimodels";

export interface StatusPercentage {
  waitingToStart: number;
  running: number;
  succeeded: number;
  failed: number;
}
export function calculateStatusPercentage(
  runSummaryDto: Pick<
    RunSummaryDto,
    | "waitingTestCount"
    | "testCount"
    | "runningTestCount"
    | "succeededTestCount"
    | "failedTestCount"
  >
): StatusPercentage {
  return {
    waitingToStart:
      (runSummaryDto.waitingTestCount / runSummaryDto.testCount) * 100,
    running: (runSummaryDto.runningTestCount / runSummaryDto.testCount) * 100,
    succeeded:
      (runSummaryDto.succeededTestCount / runSummaryDto.testCount) * 100,
    failed: (runSummaryDto.failedTestCount / runSummaryDto.testCount) * 100,
  };
}
