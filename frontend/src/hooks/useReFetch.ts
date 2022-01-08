import { useCallback, useEffect, useState } from "react";
import { useInterval } from "rooks";
import { FetchResult } from "./useFetch";
interface UseReFetchResult<T> {
  data?: T;
  isLoading: boolean;
  error?: Error;
}

export function useReFetch<TData = any>(
  url: string,
  interval: number,
  dependencies?: any[]
): UseReFetchResult<TData> {
  const [isFirstFetch, setFirstFetch] = useState(true);
  const markFirstFetch = useCallback(() => {
    if (isFirstFetch) {
      setFirstFetch(false);
    }
  }, [isFirstFetch]);
  const [fetchResult, setFetchResult] = useState<FetchResult<TData>>({
    isLoading: true,
    data: undefined,
    error: undefined,
  });

  const doFetch = useCallback(() => {
    fetch(url)
      .then((res) => {
        markFirstFetch();
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
          });
        },
        (error: Error) =>
          setFetchResult({
            isLoading: false,
            data: undefined,
            error: error,
          })
      );
  }, [markFirstFetch, url]);

  useEffect(() => {
    doFetch();
  }, [...(dependencies || []), doFetch, setFetchResult]);

  const [start] = useInterval(
    () => {
      if (!fetchResult.isLoading) {
        doFetch();
      }
    },
    interval,
    true
  );
  start();
  return {
    data: fetchResult.data,
    isLoading: isFirstFetch ? fetchResult.isLoading : false,
    error: fetchResult.error,
  };
}
