import { calculateStatusPercentage } from "./utils";

describe("Run Summary utils", () => {
  it("should calculate status percentage correctly", () => {
    const statusPercentage = calculateStatusPercentage({
      test_count: 10,
      waiting_test_count: 2,
      running_test_count: 3,
      failed_test_count: 4,
      succeeded_test_count: 1,
    });

    expect(statusPercentage).toStrictEqual({
      waitingToStart: 20,
      running: 30,
      failed: 40,
      succeeded: 10,
    });
  });
});
