import { RunSummaryDto } from "../../../../catoapimodels";
export interface StatusPercentage {
  waitingToStart: number;
  running: number;
  succeeded: number;
  failed: number;
}
export function calculateStatusPercentage(
  runSummaryDto: RunSummaryDto
): StatusPercentage {
  return {
    waitingToStart:
      (runSummaryDto.waiting_test_count / runSummaryDto.test_count) * 100,
    running:
      (runSummaryDto.running_test_count / runSummaryDto.test_count) * 100,
    succeeded:
      (runSummaryDto.succeeded_test_count / runSummaryDto.test_count) * 100,
    failed: (runSummaryDto.failed_test_count / runSummaryDto.test_count) * 100,
  };
}
