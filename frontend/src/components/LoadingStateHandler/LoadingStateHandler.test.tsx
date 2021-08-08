import {
  DataLoadedState,
  ErrorState,
  LoadingState,
  LoadingStateHandler,
} from "./LoadingStateHandler";
import { render } from "@testing-library/react";

describe("LoadingStateHandler", () => {
  describe("LoadingState", () => {
    it("should render defined LoadingState when loading is true", () => {
      const rendered = render(
        <LoadingStateHandler isLoading={true}>
          <LoadingState>Loading</LoadingState>
        </LoadingStateHandler>
      );

      expect(rendered.getByText("Loading")).toBeInTheDocument();
    });

    it("should not render defined LoadingState when loading is true", () => {
      const rendered = render(
        <LoadingStateHandler isLoading={false}>
          <LoadingState>Loading</LoadingState>
        </LoadingStateHandler>
      );

      expect(rendered.queryByText("Loading")).not.toBeInTheDocument();
    });

    it("should render nothing when loading is true and no LoadingState is defined", () => {
      const rendered = render(<LoadingStateHandler isLoading={false} />);

      expect(rendered.container.children.length).toBe(0);
    });
  });
  describe("ErrorState", () => {
    it("should render defined ErrorState when there is an Error", () => {
      const rendered = render(
        <LoadingStateHandler isLoading={false} error={new Error()}>
          <ErrorState>Error</ErrorState>
        </LoadingStateHandler>
      );

      expect(rendered.getByText("Error")).toBeInTheDocument();
    });

    it("should not render defined ErrorState when there is no error", () => {
      const rendered = render(
        <LoadingStateHandler isLoading={false}>
          <ErrorState>Error</ErrorState>
        </LoadingStateHandler>
      );

      expect(rendered.queryByText("Error")).not.toBeInTheDocument();
    });

    it("should render nothing when there is an Error but no Error State defined", () => {
      const rendered = render(
        <LoadingStateHandler isLoading={false} error={new Error()} />
      );

      expect(rendered.container.children.length).toBe(0);
    });
  });
  describe("DataLoadedState", () => {
    it("should render defined DataLoadedState when isLoaded and there is no error", () => {
      const rendered = render(
        <LoadingStateHandler isLoading={false}>
          <DataLoadedState>Data</DataLoadedState>
        </LoadingStateHandler>
      );

      expect(rendered.getByText("Data")).toBeInTheDocument();
    });

    it("should not render defined DataLoadedState when data is loading and there is no error", () => {
      const rendered = render(
        <LoadingStateHandler isLoading={true}>
          <DataLoadedState>Data</DataLoadedState>
        </LoadingStateHandler>
      );

      expect(rendered.queryByText("Data")).not.toBeInTheDocument();
    });

    it("should not render defined DataLoadedState when data is loading and there is an error", () => {
      const rendered = render(
        <LoadingStateHandler isLoading={true} error={new Error()}>
          <DataLoadedState>Data</DataLoadedState>
        </LoadingStateHandler>
      );

      expect(rendered.queryByText("Error")).not.toBeInTheDocument();
    });

    it("should render nothing when data is loaded but no DataLoadedState is defined", () => {
      const rendered = render(<LoadingStateHandler isLoading={true} />);

      expect(rendered.container.children.length).toBe(0);
    });
  });

  describe("all states combined", () => {
    it("should render LoadingState", () => {
      const rendered = render(
        <LoadingStateHandler isLoading={true}>
          <LoadingState>Loading</LoadingState>
          <ErrorState>Error</ErrorState>
          <DataLoadedState>Data</DataLoadedState>
        </LoadingStateHandler>
      );

      expect(rendered.getByText("Loading")).toBeInTheDocument();
    });
    it("should render ErrorState", () => {
      const rendered = render(
        <LoadingStateHandler isLoading={false} error={new Error()}>
          <LoadingState>Loading</LoadingState>
          <ErrorState>Error</ErrorState>
          <DataLoadedState>Data</DataLoadedState>
        </LoadingStateHandler>
      );

      expect(rendered.getByText("Error")).toBeInTheDocument();
    });
    it("should render DataLoadedState", () => {
      const rendered = render(
        <LoadingStateHandler isLoading={false}>
          <LoadingState>Loading</LoadingState>
          <ErrorState>Error</ErrorState>
          <DataLoadedState>Data</DataLoadedState>
        </LoadingStateHandler>
      );

      expect(rendered.getByText("Data")).toBeInTheDocument();
    });
  });
});
