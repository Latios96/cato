import { renderIf } from "./utils";
import React from "react";
import { render } from "@testing-library/react";

interface Props {
  value?: string;
}

const TestingComponent = (props: Props) => {
  return (
    <div>
      {renderIf(props.value, (v) => {
        return <h1 data-testid={"test"}>{v}</h1>;
      })}
    </div>
  );
};

describe("renderIf", () => {
  it("should render empty when value is falsy", () => {
    const rendered = render(<TestingComponent />);
    expect(rendered.queryByTestId("test")).not.toBeInTheDocument();
  });

  it("should render callback result", () => {
    const rendered = render(<TestingComponent value={"testvalue"} />);
    expect(rendered.queryByTestId("test")).toBeInTheDocument();
  });
});
