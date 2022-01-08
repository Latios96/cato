import { useEffect, useState } from "react";

export interface FetchResult<T> {
  data?: T;
  error?: Error;
  isLoading: boolean;
}

export function useFetch<T>(url: string): FetchResult<T> {
  const [fetchResult, setFetchResult] = useState<FetchResult<T>>({
    isLoading: true,
    data: undefined,
    error: undefined,
  });

  useEffect(() => {
    fetch(url)
      .then((res) => res.json())
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
  }, [url, setFetchResult]);

  return fetchResult;
}
