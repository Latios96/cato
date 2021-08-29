export enum StatusFilter {
  NONE = "NONE",
  NOT_STARTED = "NOT_STARTED",
  RUNNING = "RUNNING",
  FAILED = "FAILED",
  SUCCESS = "SUCCESS",
}

export class FilterOptions {
  constructor(status?: StatusFilter) {
    if (status) {
      this.status = status;
    }
  }

  public status: StatusFilter = StatusFilter.NONE;
}
