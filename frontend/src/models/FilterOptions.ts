import {
  StatusFilter,
  TestFailureReason,
} from "../catoapimodels/catoapimodels";

export class FilterOptions {
  constructor(status?: StatusFilter, failureReason?: TestFailureReason) {
    if (status) {
      this.status = status;
    }
    this.failureReason = failureReason;
  }

  public status: StatusFilter = StatusFilter.NONE;
  public failureReason?: TestFailureReason = undefined;

  public withChangedStatusFilter(statusFilter: StatusFilter): FilterOptions {
    return new FilterOptions(statusFilter, this.failureReason);
  }
  public withChangedFailureReason(
    failureReason?: TestFailureReason
  ): FilterOptions {
    return new FilterOptions(this.status, failureReason);
  }
}
