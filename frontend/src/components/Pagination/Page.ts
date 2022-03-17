export interface Page<T extends Object> {
  pageNumber: number;
  pageSize: number;
  totalEntityCount: number;
  entities: T[];
}
export interface ControllablePage {
  pageNumber: number;
  pageSize: number;
  totalEntityCount: number;
}
export interface PageRequest {
  pageNumber: number;
  pageSize: number;
}

export function requestFirstPageOfSize(size: number): PageRequest {
  return { pageNumber: 1, pageSize: size };
}

export function firstEntityOnPage(page: ControllablePage) {
  return page.pageSize * (page.pageNumber - 1) + 1;
}

export function lastEntityOnPage(page: ControllablePage) {
  const lastEntity = page.pageSize * page.pageNumber;
  if (lastEntity > page.totalEntityCount) {
    return page.totalEntityCount;
  }
  return lastEntity;
}

export function totalPages(page: ControllablePage) {
  let totalPages = Math.ceil(page.totalEntityCount / page.pageSize);
  if (totalPages === 0) {
    totalPages = 1;
  }
  return totalPages;
}
