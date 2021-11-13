import { TestFailureReasonDto } from "../catoapimodels";

export enum StatusFilter {
  NONE = "NONE",
  NOT_STARTED = "NOT_STARTED",
  RUNNING = "RUNNING",
  FAILED = "FAILED",
  SUCCESS = "SUCCESS",
}

export class FilterOptions {
  constructor(status?: StatusFilter, failureReason?: TestFailureReasonDto) {
    if (status) {
      this.status = status;
    }
    this.failureReason = failureReason;
  }

  public status: StatusFilter = StatusFilter.NONE;
  public failureReason?: TestFailureReasonDto = undefined;

  public withChangedStatusFilter(statusFilter: StatusFilter): FilterOptions {
    return new FilterOptions(statusFilter, this.failureReason);
  }
  public withChangedFailureReason(
    failureReason?: TestFailureReasonDto
  ): FilterOptions {
    return new FilterOptions(this.status, failureReason);
  }
}
