import React, { useEffect, useState } from "react";
export function renderIf<T>(
  value: T | null | undefined,
  renderCallback: (value: T) => JSX.Element
): JSX.Element {
  if (value !== undefined && value !== null) {
    return renderCallback(value);
  }
  return <React.Fragment />;
}

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
