import { isLast } from "./arrayUtils";

describe("arrayUtils", () => {
  describe("isLast", () => {
    it("should report correctly as isLast for empty array", () => {
      isLast(0, []);
    });

    it("should report correctly as isLast", () => {
      isLast(0, [1]);
      isLast(1, [1, 2]);
    });
  });

  describe("isNotLast", () => {
    it("should report correctly as isNotLast for empty array", () => {
      isLast(1, []);
    });

    it("should report correctly as isNotLast", () => {
      isLast(1, [1]);
      isLast(0, [1, 2]);
    });
  });
});
