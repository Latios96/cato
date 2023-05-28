import React from "react";
import BasicPage from "../BasicPage";
import ProjectInformation from "./internal/ProjectInformation";
import styles from "./ProjectPage.module.scss";
import { useFetch } from "use-http";
import { Project, RunBatchAggregate } from "../../catoapimodels/catoapimodels";
import { useHistory } from "react-router-dom";
import { parseStateFromQueryString } from "./internal/RunBatchList/queryStringState";
import { useReFetch } from "../../hooks/useReFetch";
import { Page } from "../../components/Pagination/Page";
import { toCommaSeparatedString } from "./internal/utils";
import {
  popFromQueryString,
  updateQueryString,
} from "../../utils/queryStringUtils";
import RunBatchList from "./internal/RunBatchList/RunBatchList";
interface Props {
  projectId: number;
}

function ProjectPage(props: Props) {
  const { loading: projectIsLoading, data: project } = useFetch<Project>(
    "/api/v1/projects/" + props.projectId,
    []
  );

  const history = useHistory();
  const state = parseStateFromQueryString(history.location.search);

  const {
    isLoading: loadingRuns,
    error: errorRuns,
    data: runs,
  } = useReFetch<Page<RunBatchAggregate>>(
    `/api/v1/run_batches/project/${props.projectId}?pageNumber=${
      state.page.pageNumber
    }&pageSize=${state.page.pageSize}&branches=${toCommaSeparatedString(
      state.branches
    )}`,
    5000,
    [
      state.page.pageSize,
      state.page.pageNumber,
      toCommaSeparatedString(state.branches),
    ]
  );

  const { data: branches } = useReFetch<string[]>(
    `/api/v1/runs/project/${props.projectId}/branches`,
    5000,
    []
  );

  const isLoading = loadingRuns || projectIsLoading;

  return (
    <BasicPage>
      <div className={styles.projectPageScroll}>
        <ProjectInformation project={project} isLoading={isLoading} />
        <div
          className={"ml-auto mr-auto "}
          style={{ width: "850px", marginTop: "35px" }}
        ></div>
        <RunBatchList
          projectId={props.projectId}
          runs={runs}
          isLoading={isLoading}
          error={errorRuns}
          pageChanged={(page) => {
            history.push({
              // todo can we make this better?
              search: updateQueryString(history.location.search, {
                pageNumber: page.pageNumber,
                pageSize: page.pageSize,
              }),
            });
          }}
          filteredBranchesChanged={(branches) => {
            let search = "";
            if (!branches.size) {
              search = popFromQueryString(history.location.search, [
                "branches",
              ]);
            } else {
              search = updateQueryString(history.location.search, {
                branches: Array.from(branches).sort().join(","),
              });
            }
            history.push({ search });
          }}
          branches={branches || []}
          selectedBranches={state.branches}
        />
      </div>
    </BasicPage>
  );
}

export default ProjectPage;
