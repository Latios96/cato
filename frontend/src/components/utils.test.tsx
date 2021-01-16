import { mount } from "enzyme";
import { renderIf } from "./utils";
import React from "react";

interface Props {
  value?: string;
}

const TestingComponent = (props: Props) => {
  return (
    <div>
      {renderIf(props.value, (v) => {
        return <h1>{v}</h1>;
      })}
    </div>
  );
};

describe("renderIf", () => {
  it("should render empty when value is falsy", () => {
    const testingComponent = mount(<TestingComponent />);
    expect(testingComponent).toMatchSnapshot();
  });

  it("should render callback result", () => {
    const testingComponent = mount(<TestingComponent value={"test"} />);
    expect(testingComponent).toMatchSnapshot();
  });
});
