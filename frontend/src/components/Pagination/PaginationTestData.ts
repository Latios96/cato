export const smallPage = {
  pageNumber: 1,
  pageSize: 10,
  totalEntityCount: 10,
  entities: [{ id: 1, name: "test" }],
};

export const firstPage = {
  pageNumber: 1,
  pageSize: 10,
  totalEntityCount: 100,
  entities: [{ id: 1, name: "test" }],
};

export const middlePage = {
  pageNumber: 5,
  pageSize: 1,
  totalEntityCount: 10,
  entities: [{ id: 1, name: "test" }],
};

export const lastPageWithSomePlaces = {
  pageNumber: 10,
  pageSize: 5,
  totalEntityCount: 46,
  entities: [{ id: 1, name: "test" }],
};

export const lastPageFittingExactly = {
  pageNumber: 10,
  pageSize: 1,
  totalEntityCount: 10,
  entities: [{ id: 1, name: "test" }],
};
