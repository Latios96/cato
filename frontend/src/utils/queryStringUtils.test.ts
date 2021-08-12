import { popFromQueryString, updateQueryString } from "./queryStringUtils";

describe("query string utils", () => {
  describe("update query string", () => {
    it("should insert new values into query string", () => {
      const data = { test: "myValue" };
      const queryString = "";

      const newQueryString = updateQueryString(queryString, data);

      expect(newQueryString).toBe("test=myValue");
    });

    it("should update existing values", () => {
      const data = { test: "myNewValue" };
      const queryString = "test=myValue";

      const newQueryString = updateQueryString(queryString, data);

      expect(newQueryString).toBe("test=myNewValue");
    });

    it("should keep not affected values", () => {
      const data = { newTest: "myNewValue" };
      const queryString = "test=myValue";

      const newQueryString = updateQueryString(queryString, data);

      expect(newQueryString).toBe("newTest=myNewValue&test=myValue");
    });
  });
  describe("pop from query string", () => {
    it("should pop keys from query string", () => {
      const queryString = "test=myValue";
      const keys = ["test"];

      const newQueryString = popFromQueryString(queryString, keys);

      expect(newQueryString).toBe("");
    });

    it("should keep not affected", () => {
      const queryString = "test=myValue&myOtherKey=myOtherValue";
      const keys = ["test"];

      const newQueryString = popFromQueryString(queryString, keys);

      expect(newQueryString).toBe("myOtherKey=myOtherValue");
    });
  });
});
