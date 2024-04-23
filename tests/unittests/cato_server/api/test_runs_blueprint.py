def test_get_run_by_project_id_should_return(client_with_session, project, run):
    url = "/api/v1/runs/project/{}/aggregate".format(project.id)

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [
            {
                "id": 1,
                "projectId": 1,
                "createdAt": run.created_at.isoformat(),
                "status": "NOT_STARTED",
                "duration": 0,
                "branchName": "default",
                "runInformation": {
                    "computerName": "cray",
                    "id": 1,
                    "localUsername": "username",
                    "os": "WINDOWS",
                    "runId": 1,
                    "runInformationType": "LOCAL_COMPUTER",
                },
                "suiteCount": 0,
                "testCount": 0,
                "progress": {
                    "failedTestCount": 0,
                    "progressPercentage": 0,
                    "runningTestCount": 0,
                    "succeededTestCount": 0,
                    "waitingTestCount": 0,
                },
                "performanceTraceId": None,
            }
        ],
        "pageNumber": 1,
        "pageSize": 30,
        "totalEntityCount": 1,
    }


def test_get_run_by_project_id_should_return_empty_list(client_with_session, project):
    url = "/api/v1/runs/project/{}/aggregate".format(project.id)

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [],
        "pageNumber": 1,
        "pageSize": 30,
        "totalEntityCount": 0,
    }


def test_get_run_by_project_id_paged_should_return(client_with_session, project, run):
    url = "/api/v1/runs/project/{}/aggregate?pageNumber=1&pageSize=10".format(
        project.id
    )

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert {
        "entities": [
            {
                "id": 1,
                "projectId": 1,
                "createdAt": run.created_at.isoformat(),
                "status": "NOT_STARTED",
                "duration": 0,
                "branchName": "default",
                "runInformation": {
                    "computerName": "cray",
                    "id": 1,
                    "localUsername": "username",
                    "os": "WINDOWS",
                    "runId": 1,
                    "runInformationType": "LOCAL_COMPUTER",
                },
                "suiteCount": 0,
                "testCount": 0,
                "progress": {
                    "failedTestCount": 0,
                    "progressPercentage": 0,
                    "runningTestCount": 0,
                    "succeededTestCount": 0,
                    "waitingTestCount": 0,
                },
                "performanceTraceId": None,
            }
        ],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 1,
    } == rv.json()


def test_get_run_by_project_id_paged_filtered_by_non_existing_branch_name_should_return_empty(
    client_with_session, project, run
):
    url = (
        "/api/v1/runs/project/{}/aggregate?pageNumber=1&pageSize=10&branches={}".format(
            project.id, "test"
        )
    )

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 0,
    }


def test_get_run_by_project_id_paged_filtered_by_existing_branch_name_should_return(
    client_with_session, project, run
):
    url = (
        "/api/v1/runs/project/{}/aggregate?pageNumber=1&pageSize=10&branches={}".format(
            project.id, "default"
        )
    )

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [
            {
                "id": 1,
                "projectId": 1,
                "createdAt": run.created_at.isoformat(),
                "status": "NOT_STARTED",
                "duration": 0,
                "branchName": "default",
                "runInformation": {
                    "computerName": "cray",
                    "id": 1,
                    "localUsername": "username",
                    "os": "WINDOWS",
                    "runId": 1,
                    "runInformationType": "LOCAL_COMPUTER",
                },
                "suiteCount": 0,
                "testCount": 0,
                "progress": {
                    "failedTestCount": 0,
                    "progressPercentage": 0,
                    "runningTestCount": 0,
                    "succeededTestCount": 0,
                    "waitingTestCount": 0,
                },
                "performanceTraceId": None,
            }
        ],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 1,
    }


def test_get_run_by_project_id_pages_should_return_empty_page(
    client_with_session, project
):
    url = "/api/v1/runs/project/{}/aggregate?pageNumber=1&pageSize=10".format(
        project.id
    )

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 0,
    }


def test_get_run_summary(client_with_session, run, test_result):
    rv = client_with_session.get(f"/api/v1/runs/{run.id}/aggregate")

    assert rv.json() == {
        "id": 1,
        "projectId": 1,
        "createdAt": run.created_at.isoformat(),
        "status": "NOT_STARTED",
        "duration": 5.0,
        "branchName": "default",
        "runInformation": {
            "computerName": "cray",
            "id": 1,
            "localUsername": "username",
            "os": "WINDOWS",
            "runId": 1,
            "runInformationType": "LOCAL_COMPUTER",
        },
        "suiteCount": 1,
        "testCount": 1,
        "progress": {
            "waitingTestCount": 1,
            "failedTestCount": 0,
            "runningTestCount": 0,
            "succeededTestCount": 0,
            "progressPercentage": 0.0,
        },
        "performanceTraceId": None,
    }

    assert rv.status_code == 200


def test_get_run_summary_should_error(client_with_session):
    rv = client_with_session.get("/api/v1/runs/42/summary")

    assert rv.status_code == 404


def test_run_id_exists_success(client_with_session, run):
    rv = client_with_session.get(f"/api/v1/runs/{run.id}/exists")

    assert rv.status_code == 200


def test_run_id_exists_failure(client_with_session):
    rv = client_with_session.get("/api/v1/runs/42/exists")

    assert rv.status_code == 404


def test_get_empty_branch_list(client_with_session, project):
    rv = client_with_session.get(f"/api/v1/runs/project/{project.id}/branches")

    assert rv.status_code == 200
    assert rv.json() == []


def test_get_branch_list_with_default_branch(client_with_session, project, run):
    rv = client_with_session.get(f"/api/v1/runs/project/{project.id}/branches")

    assert rv.status_code == 200
    assert rv.json() == ["default"]


CREATE_RUN_PAYLOAD_TEMPLATE = {
    "projectId": 1,
    "runBatchIdentifier": {
        "provider": "LOCAL_COMPUTER",
        "runName": "mac-os",
        "runIdentifier": "3046812908-1",
    },
    "testSuites": [
        {
            "suiteName": "my_suite",
            "suiteVariables": {},
            "tests": [
                {
                    "testName": "test_name",
                    "testIdentifier": "test/identifier",
                    "testCommand": "cmd",
                    "testVariables": {},
                    "machineInfo": {
                        "cpuName": "test",
                        "cores": 8,
                        "memory": 8,
                    },
                    "comparisonSettings": {
                        "method": "SSIM",
                        "threshold": 1,
                    },
                }
            ],
        }
    ],
}


def test_create_run_with_local_computer_run_information(
    client_with_session,
    project,
    run_batch_identifier,
    local_computer_run_information,
    object_mapper,
):
    payload = CREATE_RUN_PAYLOAD_TEMPLATE.copy()
    payload["runInformation"] = object_mapper.to_dict(local_computer_run_information)

    rv = client_with_session.post("/api/v1/runs", json=payload)

    assert rv.status_code == 201
    response_json = rv.json()
    assert response_json["runInformation"]["runInformationType"] == "LOCAL_COMPUTER"
    assert response_json["runInformation"]["runId"] == response_json["id"]


def test_create_run_with_github_actions_run_information(
    client_with_session,
    project,
    run_batch_identifier,
    github_actions_run_information,
    object_mapper,
):
    payload = CREATE_RUN_PAYLOAD_TEMPLATE.copy()
    payload["runInformation"] = object_mapper.to_dict(github_actions_run_information)

    rv = client_with_session.post("/api/v1/runs", json=payload)

    assert rv.status_code == 201
    response_json = rv.json()
    assert response_json["runInformation"]["runInformationType"] == "GITHUB_ACTIONS"
    assert response_json["runInformation"]["runId"] == response_json["id"]


class TestCreatePerformanceTrace:
    def test_success(self, client_with_session, run):
        payload = {
            "performance_trace_json": """{"traceEvents":[]}""",
        }

        rv = client_with_session.post(
            f"/api/v1/runs/{run.id}/performance_trace", json=payload
        )

        assert rv.status_code == 201
        response_json = rv.json()
        assert response_json == {"id": 1}

    def test_wrong_payload(self, client_with_session, run):
        payload = {}

        rv = client_with_session.post(
            f"/api/v1/runs/{run.id}/performance_trace", json=payload
        )

        assert rv.status_code == 400
        response_json = rv.json()
        assert response_json == {"performance_trace_json": "missing"}

    def test_not_existing_run(self, client_with_session):
        payload = {
            "performance_trace_json": """{"traceEvents":[]}""",
        }

        rv = client_with_session.post(f"/api/v1/runs/1/performance_trace", json=payload)

        assert rv.status_code == 404
        response_json = rv.json()
        assert response_json == {"run_id": "no run found"}


class TestGetPerformanceTrace:

    def test_get_success(
        self, client_with_session, run, sqlalchemy_run_repository, performance_trace
    ):
        run.performance_trace_id = performance_trace.id
        sqlalchemy_run_repository.save(run)

        rv = client_with_session.get(f"/api/v1/runs/{run.id}/performance_trace")
        assert rv.status_code == 200
        assert (
            rv.content
            == b'{"traceEvents":[{"name":"Cato Run","ph":"B","pid":0,"tid":0,"ts":0.0},{"name":"Create run in DB","ph":"B","pid":0,"tid":0,"ts":0.0},{"name":"Create run in DB","ph":"E","pid":0,"tid":0,"ts":122204.5},{"name":"Suite exr","ph":"B","pid":0,"tid":0,"ts":122204.5},{"name":"Test exr/exr_singlechannel_16_bit","ph":"B","pid":0,"tid":0,"ts":122204.5},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":122204.5},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":1523898.25},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":1552367.75},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":1612882.5},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":1615882.5},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":1882379.25},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":1882379.25},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":3007458.5},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":3007458.5},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":4136254.5},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":4136254.5},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":5265385.5},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":5266385.0},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":5314464.75},{"name":"Test exr/exr_singlechannel_16_bit","ph":"E","pid":0,"tid":0,"ts":5314464.75},{"name":"Test exr/exr_singlechannel_32_bit","ph":"B","pid":0,"tid":0,"ts":5314464.75},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":5314464.75},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":5335464.0},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":5364463.5},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":5435005.75},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":5436006.0},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":5739956.5},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":5739956.5},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":6896781.75},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":6896781.75},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":8052670.75},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":8052670.75},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":9179739.5},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":9179739.5},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":9226739.5},{"name":"Test exr/exr_singlechannel_32_bit","ph":"E","pid":0,"tid":0,"ts":9226739.5},{"name":"Test exr/exr_multichannel_16_bit_1080p","ph":"B","pid":0,"tid":0,"ts":9226739.5},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":9226739.5},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":9248468.25},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":9275476.25},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":9346476.5},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":9347476.5},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":11645006.0},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":11645006.0},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":14261094.0},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":14261094.0},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":16861761.5},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":16861761.5},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":18025417.75},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":18026418.5},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":18073941.25},{"name":"Test exr/exr_multichannel_16_bit_1080p","ph":"E","pid":0,"tid":0,"ts":18073941.25},{"name":"Test exr/exr_multichannel_16_bit","ph":"B","pid":0,"tid":0,"ts":18073941.25},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":18073941.25},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":18095935.75},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":18124449.0},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":18189316.5},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":18190316.25},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":19979901.25},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":19979901.25},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":28698599.25},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":28698599.25},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":37419699.75},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":37419699.75},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":38570678.25},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":38571678.25},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":38618680.75},{"name":"Test exr/exr_multichannel_16_bit","ph":"E","pid":0,"tid":0,"ts":38618680.75},{"name":"Suite exr","ph":"E","pid":0,"tid":0,"ts":38618680.75},{"name":"Suite jpg","ph":"B","pid":0,"tid":0,"ts":38618680.75},{"name":"Test jpg/jpeg","ph":"B","pid":0,"tid":0,"ts":38618680.75},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":38618680.75},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":38641678.75},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":38669209.0},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":38730218.75},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":38730218.75},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":38885054.0},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":38885054.0},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":41046643.5},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":41046643.5},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":42163911.25},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":42163911.25},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":43299748.75},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":43299748.75},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":43346921.25},{"name":"Test jpg/jpeg","ph":"E","pid":0,"tid":0,"ts":43347918.5},{"name":"Suite jpg","ph":"E","pid":0,"tid":0,"ts":43347918.5},{"name":"Suite png","ph":"B","pid":0,"tid":0,"ts":43347918.5},{"name":"Test png/png_8_bit","ph":"B","pid":0,"tid":0,"ts":43347918.5},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":43347918.5},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":43369918.5},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":43398435.25},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":43461347.75},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":43461347.75},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":43667947.25},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":43667947.25},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":44800511.0},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":44800511.0},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":45943589.5},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":45943589.5},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":47069490.5},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":47070490.0},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":47117492.0},{"name":"Test png/png_8_bit","ph":"E","pid":0,"tid":0,"ts":47117492.0},{"name":"Test png/png_16_bit","ph":"B","pid":0,"tid":0,"ts":47117492.0},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":47117492.0},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":47139498.5},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":47167498.0},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":47228928.5},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":47229458.75},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":47502471.75},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":47502471.75},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":48650610.0},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":48650610.0},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":49795284.25},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":49795284.25},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":50949031.75},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":50950031.5},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":50997010.25},{"name":"Test png/png_16_bit","ph":"E","pid":0,"tid":0,"ts":50997010.25},{"name":"Suite png","ph":"E","pid":0,"tid":0,"ts":50997010.25},{"name":"Suite tiff","ph":"B","pid":0,"tid":0,"ts":50997010.25},{"name":"Test tiff/tiff_8_bit","ph":"B","pid":0,"tid":0,"ts":50998008.75},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":50998008.75},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":51019007.0},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":51046017.0},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":51108419.25},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":51109419.25},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":51308107.75},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":51308107.75},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":52470686.0},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":52470686.0},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":53640037.25},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":53640037.25},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":54774310.0},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":54775310.75},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":54823425.5},{"name":"Test tiff/tiff_8_bit","ph":"E","pid":0,"tid":0,"ts":54823425.5},{"name":"Test tiff/tiff_16_bit","ph":"B","pid":0,"tid":0,"ts":54823425.5},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":54823425.5},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":54845425.25},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":54873436.25},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":54938036.75},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":54939035.75},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":55176540.75},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":55176540.75},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":56377314.0},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":56377314.0},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":57576304.5},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":57576304.5},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":58716805.75},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":58717806.25},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":58763937.0},{"name":"Test tiff/tiff_16_bit","ph":"E","pid":0,"tid":0,"ts":58763937.0},{"name":"Suite tiff","ph":"E","pid":0,"tid":0,"ts":58763937.0},{"name":"Cato Run","ph":"E","pid":0,"tid":0,"ts":58763937.0}]}'
        )

    def test_not_found(self, client_with_session, run):
        rv = client_with_session.get(f"/api/v1/runs/{run.id}/performance_trace")
        assert rv.status_code == 404
