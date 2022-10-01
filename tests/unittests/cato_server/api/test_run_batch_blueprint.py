from cato_common.domain.branch_name import BranchName


class TestGetRunBatchesByProjectId:
    def test_should_find_empty(self, client_with_session, project):
        rv = client_with_session.get(f"/api/v1/run_batches/project/{project.id}")

        assert rv.status_code == 200
        assert rv.json() == {
            "entities": [],
            "pageNumber": 1,
            "pageSize": 30,
            "totalEntityCount": 0,
        }

    def test_should_find_run_batch_with_local_run_information(
        self,
        client_with_session,
        saving_run_batch_factory,
        saving_run_factory,
        local_computer_run_information,
    ):
        run_batch = saving_run_batch_factory(runs=[])
        saving_run_factory(
            run_information=local_computer_run_information, run_batch_id=run_batch.id
        )

        rv = client_with_session.get(
            f"/api/v1/run_batches/project/{run_batch.project_id}"
        )

        assert rv.status_code == 200
        rv_json = rv.json()
        rv_json["entities"][0].pop("createdAt")
        rv_json["entities"][0]["runs"][0].pop("startedAt")
        assert rv_json == {
            "entities": [
                {
                    "branchName": "default",
                    "duration": 0,
                    "id": 1,
                    "progress": {
                        "failedTestCount": 0,
                        "progressPercentage": 0,
                        "runningTestCount": 0,
                        "succeededTestCount": 0,
                        "waitingTestCount": 0,
                    },
                    "projectId": 1,
                    "runBatchIdentifier": {
                        "provider": "LOCAL_COMPUTER",
                        "runIdentifier": str(
                            run_batch.run_batch_identifier.run_identifier
                        ),
                        "runName": "mac-os",
                    },
                    "runs": [
                        {
                            "branchName": "default",
                            "duration": 0,
                            "id": 1,
                            "progress": {
                                "failedTestCount": 0,
                                "progressPercentage": 0,
                                "runningTestCount": 0,
                                "succeededTestCount": 0,
                                "waitingTestCount": 0,
                            },
                            "projectId": 1,
                            "runInformation": {
                                "computerName": "cray",
                                "id": 1,
                                "localUsername": "username",
                                "os": "WINDOWS",
                                "runId": 1,
                                "runInformationType": "LOCAL_COMPUTER",
                            },
                            "status": "NOT_STARTED",
                            "suiteCount": 0,
                            "testCount": 0,
                        }
                    ],
                    "status": "NOT_STARTED",
                    "suiteCount": 0,
                    "testCount": 0,
                }
            ],
            "pageNumber": 1,
            "pageSize": 30,
            "totalEntityCount": 1,
        }

    def test_should_find_run_batch_with_github_actions_information(
        self,
        client_with_session,
        saving_run_batch_factory,
        saving_run_factory,
        github_actions_run_information,
    ):
        run_batch = saving_run_batch_factory(runs=[])
        saving_run_factory(
            run_information=github_actions_run_information, run_batch_id=run_batch.id
        )

        rv = client_with_session.get(
            f"/api/v1/run_batches/project/{run_batch.project_id}"
        )

        assert rv.status_code == 200
        rv_json = rv.json()
        rv_json["entities"][0].pop("createdAt")
        rv_json["entities"][0]["runs"][0].pop("startedAt")
        assert rv_json == {
            "entities": [
                {
                    "branchName": "default",
                    "duration": 0,
                    "id": 1,
                    "progress": {
                        "failedTestCount": 0,
                        "progressPercentage": 0,
                        "runningTestCount": 0,
                        "succeededTestCount": 0,
                        "waitingTestCount": 0,
                    },
                    "projectId": 1,
                    "runBatchIdentifier": {
                        "provider": "LOCAL_COMPUTER",
                        "runIdentifier": str(
                            run_batch.run_batch_identifier.run_identifier
                        ),
                        "runName": "mac-os",
                    },
                    "runs": [
                        {
                            "branchName": "default",
                            "duration": 0,
                            "id": 1,
                            "progress": {
                                "failedTestCount": 0,
                                "progressPercentage": 0,
                                "runningTestCount": 0,
                                "succeededTestCount": 0,
                                "waitingTestCount": 0,
                            },
                            "projectId": 1,
                            "runInformation": {
                                "actor": "Latios96",
                                "attempt": 1,
                                "computerName": "cray",
                                "githubApiUrl": "https://api.github.com",
                                "githubRunId": 3052454707,
                                "githubUrl": "https://github.com",
                                "htmlUrl": "https://github.com/owner/repo-name/actions/runs/3052454707/jobs/4921861789",
                                "id": 1,
                                "jobName": "build_ubuntu",
                                "os": "LINUX",
                                "runId": 1,
                                "runInformationType": "GITHUB_ACTIONS",
                                "runNumber": 2,
                            },
                            "status": "NOT_STARTED",
                            "suiteCount": 0,
                            "testCount": 0,
                        }
                    ],
                    "status": "NOT_STARTED",
                    "suiteCount": 0,
                    "testCount": 0,
                }
            ],
            "pageNumber": 1,
            "pageSize": 30,
            "totalEntityCount": 1,
        }

    def test_should_find_with_pagination(
        self, client_with_session, project, saving_run_batch_factory
    ):
        for i in range(20):
            saving_run_batch_factory()

        rv = client_with_session.get(
            f"/api/v1/run_batches/project/{project.id}?pageNumber=1&pageSize=10"
        )

        assert rv.status_code == 200
        rv_json = rv.json()
        assert len(rv_json["entities"]) == 10
        assert rv_json["pageSize"] == 10
        assert rv_json["totalEntityCount"] == 20

    def test_should_find_with_branch_filtering(
        self,
        client_with_session,
        project,
        saving_run_batch_factory,
        sqlalchemy_run_repository,
        run_factory,
    ):
        run_batch = saving_run_batch_factory()
        sqlalchemy_run_repository.insert_many(
            [
                run_factory(
                    project_id=project.id, branch_name=x, run_batch_id=run_batch.id
                )
                for x in [
                    BranchName("main"),
                    BranchName("dev"),
                ]
            ]
        )

        rv = client_with_session.get(
            f"/api/v1/run_batches/project/{project.id}?branches=main"
        )

        assert rv.status_code == 200
        rv_json = rv.json()
        assert len(rv_json["entities"]) == 1
        assert rv_json["pageSize"] == 30
        assert rv_json["totalEntityCount"] == 1
