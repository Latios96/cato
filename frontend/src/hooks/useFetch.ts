import { useEffect, useState } from "react";

export interface FetchResult<T> {
  data?: T;
  error?: string;
  isLoading: boolean;
}

export function useFetch<T>(url: string): FetchResult<T> {
  const [fetchResult, setFetchResult] = useState({
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
        (error) =>
          setFetchResult({
            isLoading: false,
            data: undefined,
            error: error,
          })
      );
  }, [url, setFetchResult]);

  return fetchResult;
}
