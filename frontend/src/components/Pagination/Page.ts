export interface Page<T extends Object> {
  page_number: number;
  page_size: number;
  total_entity_count: number;
  entities: T[];
}
export interface ControllablePage {
  page_number: number;
  page_size: number;
  total_entity_count: number;
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
  const lastEntity = page.page_size * page.page_number;
  if (lastEntity > page.total_entity_count) {
    return page.total_entity_count;
  }
  return lastEntity;
}

export function totalPages(page: ControllablePage) {
  let totalPages = Math.ceil(page.total_entity_count / page.page_size);
  if (totalPages === 0) {
    totalPages = 1;
  }
  return totalPages;
}
