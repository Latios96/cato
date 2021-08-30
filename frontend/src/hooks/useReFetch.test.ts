import nock from "nock";
import { renderHook } from "@testing-library/react-hooks";
import { useReFetch } from "./useReFetch";
import { waitFor } from "@testing-library/react";

describe("useReFetch", () => {
  it("should be loading while fetching the value for the first time", async () => {
    nock("http://localhost").get("/").reply(200, { test: 0 });

    const { result } = renderHook(() => useReFetch("http://localhost/", 10000));

    expect(result.current.loading).toBeTruthy();
    await waitFor(() => {
      expect(result.current.loading).toBeFalsy();
      expect(result.current.data).toStrictEqual({ test: 0 });
    });
  });
  it("should refetch after the specified time amount", async () => {
    let value = 0;
    nock("http://localhost")
      .get("/")
      .times(5)
      .reply(200, () => {
        return {
          test: value++,
        };
      });

    const { result } = renderHook(() => useReFetch("http://localhost/", 500));

    expect(result.current.loading).toBeTruthy();
    await waitFor(() => {
      expect(result.current.loading).toBeFalsy();
      expect(result.current.data).toStrictEqual({ test: 0 });
    });

    await waitFor(() => {
      expect(result.current.loading).toBeFalsy();
      expect(result.current.data).toStrictEqual({ test: 1 });
    });
  });

  it("should pass the error", async () => {
    nock("http://localhost").get("/").reply(500, { test: 0 });

    const { result } = renderHook(() => useReFetch("http://localhost/", 10000));

    expect(result.current.loading).toBeTruthy();
    await waitFor(() => {
      expect(result.current.loading).toBeFalsy();
      expect(result.current.error.name).toBe("500");
    });
  });
});
