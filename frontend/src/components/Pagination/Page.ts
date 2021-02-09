export interface Page<T extends Object> {
  page_number: number;
  page_size: number;
  total_pages: number;
  entities: T[];
}
export interface ControllablePage {
  page_number: number;
  page_size: number;
  total_pages: number;
}
export interface PageRequest {
  page_number: number;
  page_size: number;
}

export function requestFirstPageOfSize(size: number): PageRequest {
  return { page_number: 1, page_size: size };
}

export function firstEntityOnPage(page: ControllablePage) {
  return page.page_size * (page.page_number - 1) + 1;
}
export function lastEntityOnPage(page: ControllablePage) {
  return page.page_size * page.page_number + 1;
}
export function totalEntities(page: ControllablePage) {
  return page.page_size * page.total_pages;
}
