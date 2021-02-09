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
      const { getByRole } = render(
        <SimplePaginationControls
          currentPage={firstPage}
          pageChangedCallback={jest.fn()}
        />
      );

      expect(getByRole("previous")).toHaveAttribute("disabled", "");
      expect(getByRole("next")).toBeEnabled();
    });

    it("should disable 'next page' on last page", () => {
      const { getByRole } = render(
        <SimplePaginationControls
          currentPage={lastPageWithSomePlaces}
          pageChangedCallback={jest.fn()}
        />
      );

      expect(getByRole("previous")).toBeEnabled();
      expect(getByRole("next")).toHaveAttribute("disabled", "");
    });

    it("should disable 'next page' and 'previous page' on small first page", () => {
      const { getByRole } = render(
        <SimplePaginationControls
          currentPage={smallPage}
          pageChangedCallback={jest.fn()}
        />
      );

      expect(getByRole("previous")).toHaveAttribute("disabled", "");
      expect(getByRole("next")).toHaveAttribute("disabled", "");
    });

    it("should enable 'next page' and 'previous page' on middle page", () => {
      const { getByRole } = render(
        <SimplePaginationControls
          currentPage={middlePage}
          pageChangedCallback={jest.fn()}
        />
      );

      expect(getByRole("previous")).toBeEnabled();
      expect(getByRole("next")).toBeEnabled();
    });
  });

  describe("changing pages", () => {
    it("should change to previous page", () => {
      const { getByRole, getByText } = render(
        <SimplePaginationControls
          currentPage={middlePage}
          pageChangedCallback={jest.fn()}
        />
      );
      expect(getByText("5-5 of 10")).toBeInTheDocument();

      getByRole("previous").click();

      expect(getByText("4-4 of 10")).toBeInTheDocument();
    });

    it("should change to next page", () => {
      const { getByRole, getByText } = render(
        <SimplePaginationControls
          currentPage={middlePage}
          pageChangedCallback={jest.fn()}
        />
      );
      expect(getByText("5-5 of 10")).toBeInTheDocument();

      getByRole("next").click();

      expect(getByText("6-6 of 10")).toBeInTheDocument();
    });
  });
});
