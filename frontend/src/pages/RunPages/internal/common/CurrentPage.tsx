export enum CurrentPage {
  OVERVIEW,
  SUITES,
  TESTS,
}

export function toDisplayString(currentPage: CurrentPage): string {
  switch (currentPage) {
    case CurrentPage.OVERVIEW:
      return "Overview";
    case CurrentPage.SUITES:
      return "Suites";
    case CurrentPage.TESTS:
      return "Tests";
  }
}
