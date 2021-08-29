import { CollectionHandler } from "./CollectionHandler";
import { render } from "@testing-library/react";

describe("CollectionHandler", () => {
  it("should render placeholder for empty data array", () => {
    const rendered = render(
      <CollectionHandler
        data={[]}
        placeHolder={<div>Placeholder</div>}
        renderElements={(data) => data.map((d) => <div>{d}</div>)}
      />
    );

    expect(rendered.getByText("Placeholder")).toBeInTheDocument();
  });

  it("should render placeholder for undefined data array", () => {
    const rendered = render(
      <CollectionHandler
        data={undefined}
        placeHolder={<div>Placeholder</div>}
        renderElements={(data) => data.map((d) => <div>{d}</div>)}
      />
    );

    expect(rendered.getByText("Placeholder")).toBeInTheDocument();
  });

  it("should render data elements", () => {
    const rendered = render(
      <CollectionHandler
        data={[1, 2, 3]}
        placeHolder={<div>Placeholder</div>}
        renderElements={(data) => data.map((d) => <div>{d}</div>)}
      />
    );

    expect(rendered.getByText("1")).toBeInTheDocument();
    expect(rendered.getByText("2")).toBeInTheDocument();
    expect(rendered.getByText("3")).toBeInTheDocument();
  });
});
