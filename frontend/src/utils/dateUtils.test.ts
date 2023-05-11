import each from "jest-each";
import { formatDuration, toHoursAndMinutes } from "./dateUtils";

describe("format duration", () => {
  each([[undefined, null, "NaN", "-1"]]).it(
    "should format %s to empty string",
    (value) => {
      expect(formatDuration(value)).toBe("");
    }
  );
  it("should format 0 to 0 seconds", () => {
    expect(formatDuration(0)).toBe("0 seconds");
  });

  it('should format 0.1 seconds to "less than one second"', () => {
    expect(formatDuration(0.1)).toBe("less than one second");
  });
});

describe("toHoursAndMinutes", () => {
  it("should format -1 to empty", () => {
    expect(toHoursAndMinutes(-1)).toBe("");
  });
  it("should format 0 to empty", () => {
    expect(toHoursAndMinutes(0)).toBe("");
  });

  it("should format 0.1 to 0.1 seconds", () => {
    expect(toHoursAndMinutes(0.1)).toBe("0.1s");
  });

  it("should format 1.1 to 1 seconds", () => {
    expect(toHoursAndMinutes(1.1)).toBe("1s");
  });

  it("should format minutes correctly", () => {
    expect(toHoursAndMinutes(61)).toBe("1min 1s");
  });

  it("should format hours correctly", () => {
    expect(toHoursAndMinutes(3661)).toBe("1h 1min 1s");
  });
});
