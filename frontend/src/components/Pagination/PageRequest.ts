export interface PageRequest {
  page_number: number;
  page_size: number;
}

export function requestFirstPageOfSize(size: number): PageRequest {
  return { page_number: 1, page_size: size };
}
