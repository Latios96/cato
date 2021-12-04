import { SelectInput } from "./SelectInput";
import { fireEvent, render } from "@testing-library/react";

describe("SelectInput", () => {
  it("should open the menu on click", () => {
    const rendered = render(
      <SelectInput title={"Title"} elements={["test1", "test2"]} />
    );
    fireEvent.click(rendered.getByText("Title"));

    expect(rendered.getByText("test1")).toBeInTheDocument();
  });

  it("should not select any element", () => {
    const rendered = render(
      <SelectInput title={"Title"} elements={["test1", "test2"]} />
    );
    fireEvent.click(rendered.getByText("Title"));

    expect(rendered.getByText("test1")).toBeInTheDocument();
    expect(rendered.queryByTestId("test1-selected")).not.toBeInTheDocument();
  });

  it("should select the provided elements", () => {
    const rendered = render(
      <SelectInput
        title={"Title"}
        elements={["test1", "test2"]}
        selectedElements={new Set(["test1"])}
      />
    );
    fireEvent.click(rendered.getByText("Title"));

    expect(rendered.getByText("test1")).toBeInTheDocument();
    expect(rendered.getByTestId("test1-selected")).toBeInTheDocument();
  });

  it("should call onChange with the newly elements", () => {
    const onChange = jest.fn();
    const rendered = render(
      <SelectInput
        title={"Title"}
        elements={["test1", "test2"]}
        onChange={onChange}
      />
    );

    fireEvent.click(rendered.getByText("Title"));
    fireEvent.click(rendered.getByText("test1"));

    expect(onChange).toBeCalledWith(new Set(["test1"]));
  });

  it("should call onChange with the removed elements", () => {
    const onChange = jest.fn();
    const rendered = render(
      <SelectInput
        title={"Title"}
        elements={["test1", "test2"]}
        onChange={onChange}
      />
    );

    fireEvent.click(rendered.getByText("Title"));
    fireEvent.click(rendered.getByText("test1"));
    fireEvent.click(rendered.getByText("test2"));
    fireEvent.click(rendered.getByText("test1"));

    expect(onChange).toBeCalledWith(new Set(["test2"]));
  });
});
