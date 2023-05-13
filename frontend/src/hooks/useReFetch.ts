import { useCallback, useEffect, useState } from "react";
import { useIntervalWhen } from "rooks";
import { FetchResult } from "./useFetch";

interface UseReFetchResult<T> extends FetchResult<T> {
  isFirstFetch: boolean;
}

export function useReFetch<TData = any>(
  url: string,
  interval: number,
  dependencies?: any[]
): FetchResult<TData> {
  const [fetchResult, setFetchResult] = useState<UseReFetchResult<TData>>({
    isLoading: true,
    data: undefined,
    error: undefined,
    isFirstFetch: true,
  });

  const doFetch = useCallback(() => {
    fetch(url)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`${res.status}: ${res.statusText}`);
        }
        return res.json() as Promise<TData>;
      })
      .then(
        (result) => {
          setFetchResult({
            isLoading: false,
            data: result,
            error: undefined,
            isFirstFetch: false,
          });
        },
        (error: Error) =>
          setFetchResult({
            isLoading: false,
            data: undefined,
            error: error,
            isFirstFetch: false,
          })
      );
  }, [url]);

  useEffect(() => {
    doFetch();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...(dependencies || []), doFetch, setFetchResult]);

  useIntervalWhen(
    () => {
      if (!fetchResult.isLoading) {
        doFetch();
      }
    },
    interval,
    true
  );

  return {
    data: fetchResult.data,
    isLoading: fetchResult.isFirstFetch ? fetchResult.isLoading : false,
    error: fetchResult.error,
  };
}
