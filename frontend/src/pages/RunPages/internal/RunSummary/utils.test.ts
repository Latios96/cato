import { calculateStatusPercentage } from "./utils";

describe("Run Summary utils", () => {
  it("should calculate status percentage correctly", () => {
    const statusPercentage = calculateStatusPercentage({
      testCount: 10,
      waitingTestCount: 2,
      runningTestCount: 3,
      failedTestCount: 4,
      succeededTestCount: 1,
    });

    expect(statusPercentage).toStrictEqual({
      waitingToStart: 20,
      running: 30,
      failed: 40,
      succeeded: 10,
    });
  });
});
