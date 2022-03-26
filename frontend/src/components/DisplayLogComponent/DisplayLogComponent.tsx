import React, { useEffect } from "react";
import LogComponent from "../LogComponent/LogComponent";
import { Button } from "react-bootstrap";
import styles from "./DisplayLogComponent.module.scss";
import { useToggle } from "rooks";
import {
  DataLoadedState,
  LoadingStateHandler,
} from "../LoadingStateHandler/LoadingStateHandler";
import { CachePolicies, useFetch } from "use-http";
interface Props {
  testResultId: number;
}
interface Output {
  id: number;
  test_result_id: number;
  text: string;
}

function DisplayLogComponent(props: Props) {
  const [expanded, toggle] = useToggle(false);
  const { data, loading, get } = useFetch<Output>(
    `/api/v1/test_results/${props.testResultId}/output`,
    {
      cachePolicy: CachePolicies.NO_CACHE,
    }
  );
  useEffect(() => {
    if (expanded) {
      get();
    }
  }, [get, expanded, props.testResultId]);

  const getButtonText = () => {
    if (loading) {
      return "Loading..";
    }
    return expanded ? "Hide Log" : "Display Log";
  };
  return (
    <div>
      <Button onClick={toggle} disabled={loading} className={styles.logButton}>
        {getButtonText()}
      </Button>
      <LoadingStateHandler isLoading={loading}>
        <DataLoadedState>
          {data && expanded ? <LogComponent content={data.text} /> : null}
        </DataLoadedState>
      </LoadingStateHandler>
    </div>
  );
}

export default DisplayLogComponent;
