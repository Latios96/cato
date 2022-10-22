import { parseStateFromQueryString } from "./queryStringState";

describe("queryStringState", () => {
  it("should parse an empty string correctly", () => {
    const state = parseStateFromQueryString("");

    expect(state).toStrictEqual({
      page: { pageNumber: 1, pageSize: 25 },
      branches: new Set<string>(),
    });
  });
  it("should parse page correctly", () => {
    const state = parseStateFromQueryString("?pageNumber=2&pageSize=20");

    expect(state).toStrictEqual({
      page: { pageNumber: 2, pageSize: 20 },
      branches: new Set<string>(),
    });
  });
  it("should parse branches correctly", () => {
    const state = parseStateFromQueryString("?branches=master,test");

    expect(state).toStrictEqual({
      page: { pageNumber: 1, pageSize: 25 },
      branches: new Set<string>(["master", "test"]),
    });
  });

  it("should parse pages and branches correctly", () => {
    const state = parseStateFromQueryString(
      "?pageNumber=2&pageSize=20&branches=master,test"
    );

    expect(state).toStrictEqual({
      page: { pageNumber: 2, pageSize: 20 },
      branches: new Set<string>(["master", "test"]),
    });
  });
});

//
//
