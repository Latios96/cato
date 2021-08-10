import SimplePaginationControls from "./SimplePaginationControls";
import {
  firstPage,
  lastPageWithSomePlaces,
  middlePage,
  smallPage,
} from "./PaginationTestData";
import { render } from "@testing-library/react";

describe("SimplePaginationControls", () => {
  describe("button state handling", () => {
    it("should disable 'previous page' on first page", () => {
      const { getByText } = render(
        <SimplePaginationControls
          currentPage={firstPage}
          pageChangedCallback={jest.fn()}
        />
      );

      expect(getByText("Previous")).not.toBeEnabled();
      expect(getByText("Next Page")).toBeEnabled();
    });

    it("should disable 'next page' on last page", () => {
      const { getByText } = render(
        <SimplePaginationControls
          currentPage={lastPageWithSomePlaces}
          pageChangedCallback={jest.fn()}
        />
      );

      expect(getByText("Previous")).toBeEnabled();
      expect(getByText("Next Page")).not.toBeEnabled();
    });

    it("should disable 'next page' and 'previous page' on small first page", () => {
      const { getByText } = render(
        <SimplePaginationControls
          currentPage={smallPage}
          pageChangedCallback={jest.fn()}
        />
      );

      expect(getByText("Previous")).not.toBeEnabled();
      expect(getByText("Next Page")).not.toBeEnabled();
    });

    it("should enable 'next page' and 'previous page' on middle page", () => {
      const { getByText } = render(
        <SimplePaginationControls
          currentPage={middlePage}
          pageChangedCallback={jest.fn()}
        />
      );

      expect(getByText("Previous")).toBeEnabled();
      expect(getByText("Next Page")).toBeEnabled();
    });
  });
});
