import { SuiteTestListImpl } from "./SuiteTestListImpl";
import { render } from "@testing-library/react";

describe("SuiteTestList", () => {
  it("should display a placeholder text for suites without tests", () => {
    const rendered = render(
      <SuiteTestListImpl
        loading={false}
        error={new Error()}
        data={[]}
        selectedTestId={1}
        onClick={jest.fn}
      />
    );

    expect(rendered.getByText("This suite has no tests")).toBeInTheDocument();
  });
});
