import React from "react";
import {
  ExecutionStatusDto,
  TestResultDto,
  TestStatusDto,
} from "../../catoapimodels";
import WaitingOrRunningTestResultComponent from "./WaitingOrRunningTestResultComponent";
import { render, screen } from "@testing-library/react";

const testResultWaitingToStart: TestResultDto = {
  id: 1,
  suite_result_id: 2,
  test_name: "testName",
  test_identifier: "mySuite/testName",
  test_command: "my command",
  test_variables: {},
  machine_info: {
    cores: 8,
    memory: 8,
    cpu_name: "test",
  },
  execution_status: ExecutionStatusDto.NOT_STARTED,
  status: TestStatusDto.FAILED,
  seconds: 1,
  message: "message",
  image_output: null,
  reference_image: null,
  started_at: null,
  finished_at: null,
};

const testResultRunning: TestResultDto = {
  id: 1,
  suite_result_id: 2,
  test_name: "testName",
  test_identifier: "mySuite/testName",
  test_command: "my command",
  test_variables: {},
  machine_info: {
    cores: 8,
    memory: 8,
    cpu_name: "test",
  },
  execution_status: ExecutionStatusDto.RUNNING,
  status: TestStatusDto.FAILED,
  seconds: 1,
  message: "message",
  image_output: null,
  reference_image: null,
  started_at: null,
  finished_at: null,
};

describe("WaitingOrRunningTestResultComponent", () => {
  it("should render TestResult waiting to start correctly", () => {
    render(
      <WaitingOrRunningTestResultComponent result={testResultWaitingToStart} />
    );

    expect(screen.queryByAltText("an animated rendering icon")).toBeNull();
    expect(screen.queryByTestId("running-hourglas")).not.toBeNull();
    expect(screen.getAllByText("waiting to start...")).not.toBeNull();
  });
  it("should render TestResult running correctly", () => {
    render(<WaitingOrRunningTestResultComponent result={testResultRunning} />);

    expect(screen.queryByAltText("an animated rendering icon")).not.toBeNull();
    expect(screen.getByText("started: unknown")).not.toBeNull();
  });
});
