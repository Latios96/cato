import { fromQueryString, toQueryString } from "./pageQueryStringUtils";

describe("pageQueryStringUtils", () => {
  it("should convert a pagerequest to a query string", () => {
    const pageRequest = {
      pageNumber: 1,
      pageSize: 25,
    };

    const theQueryString = toQueryString(pageRequest);

    expect(theQueryString).toBe("pageNumber=1&pageSize=25");
  });

  it("should parse a pagerequest from a query string", () => {
    const pageRequest = {
      pageNumber: 1,
      pageSize: 25,
    };

    const parsedResult = fromQueryString("pageNumber=1&pageSize=25");

    expect(parsedResult).toStrictEqual(pageRequest);
  });

  it("should parse a pagerequest from a query string and dont take default page", () => {
    const pageRequest = {
      pageNumber: 1,
      pageSize: 25,
    };

    const parsedResult = fromQueryString("pageNumber=1&pageSize=25", {
      pageNumber: 5,
      pageSize: 25,
    });

    expect(parsedResult).toStrictEqual(pageRequest);
  });

  it("should not parse a pagerequest from a invalid query string", () => {
    expect(() => fromQueryString("page_numbere=1&pageSize=wurst")).toThrow(
      new Error("Invalid query string: page_numbere=1&pageSize=wurst")
    );
  });

  it("should return the default page for an invalid string", () => {
    const defaultPage = {
      pageNumber: 1,
      pageSize: 25,
    };

    const parsedResult = fromQueryString(
      "pageNumber=1&pageSize=wurst",
      defaultPage
    );

    expect(parsedResult).toStrictEqual(defaultPage);
  });
});
