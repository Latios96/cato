import { fromQueryString, toQueryString } from "./pageQueryStringUtils";

describe("pageQueryStringUtils", () => {
  it("should convert a pagerequest to a query string", () => {
    const pageRequest = {
      page_number: 1,
      page_size: 25,
    };

    const theQueryString = toQueryString(pageRequest);

    expect(theQueryString).toBe("page_number=1&page_size=25");
  });

  it("should parse a pagerequest from a query string", () => {
    const pageRequest = {
      page_number: 1,
      page_size: 25,
    };

    const parsedResult = fromQueryString("page_number=1&page_size=25");

    expect(parsedResult).toStrictEqual(pageRequest);
  });

  it("should not parse a pagerequest from a invalid query string", () => {
    expect(() => fromQueryString("page_numbere=1&page_size=wurst")).toThrow(
      new Error("Invalid query string: page_numbere=1&page_size=wurst")
    );
  });
});
