import each from "jest-each";
import { formatDuration } from "./dateUtils";

describe("format duration", () => {
  each([[undefined, null, "NaN"]]).it(
    "should format %s to empty string",
    (value) => {
      expect(formatDuration(value)).toBe("");
    }
  );
  it("should format 0 to 0 seconds", () => {
    expect(formatDuration(0)).toBe("0 seconds");
  });
});
