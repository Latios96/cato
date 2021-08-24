import { CachePolicies, useFetch } from "use-http";
import { useState } from "react";
import { useInterval } from "rooks";

export function useReFetch<TData = any>(
  url: string,
  interval: number,
  dependencies?: any[]
) {
  const [isFirstFetch, setFirstFetch] = useState(true);
  const markFirstFetch = () => {
    if (isFirstFetch) {
      setFirstFetch(false);
    }
  };
  const { data, loading, error, get } = useFetch<TData>(
    url,
    {
      cachePolicy: CachePolicies.NO_CACHE,
      interceptors: {
        response: async ({ response }) => {
          const res = response;
          if (res.status === 200) {
            markFirstFetch();
          }
          return res;
        },
      },
    },
    dependencies === undefined ? [] : dependencies
  );

  const [start] = useInterval(
    () => {
      if (!loading) {
        get();
      }
    },
    interval,
    true
  );
  start();
  return { data, loading: isFirstFetch ? loading : false, error };
}
