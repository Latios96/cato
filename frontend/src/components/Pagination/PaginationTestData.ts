export const smallPage = {
  page_number: 1,
  page_size: 10,
  total_entity_count: 10,
  entities: [{ id: 1, name: "test" }],
};

export const firstPage = {
  page_number: 1,
  page_size: 10,
  total_entity_count: 100,
  entities: [{ id: 1, name: "test" }],
};

export const middlePage = {
  page_number: 5,
  page_size: 1,
  total_entity_count: 10,
  entities: [{ id: 1, name: "test" }],
};

export const lastPageWithSomePlaces = {
  page_number: 10,
  page_size: 5,
  total_entity_count: 46,
  entities: [{ id: 1, name: "test" }],
};

export const lastPageFittingExactly = {
  page_number: 10,
  page_size: 1,
  total_entity_count: 10,
  entities: [{ id: 1, name: "test" }],
};
