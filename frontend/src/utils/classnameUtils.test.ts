import { joinClassnames } from "./classnameUtils";

describe("classnameUtils", () => {
  it("should keep all string of length >0", () => {
    const joined = joinClassnames([
      "",
      "classname",
      "otherclassname",
      false,
      undefined,
      true,
    ]);

    expect(joined).toBe("classname otherclassname");
  });
});
