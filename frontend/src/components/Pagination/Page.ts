export interface Page<T extends Object> {
  page_number: number;
  page_size: number;
  total_pages: number;
  entities: T[];
}
