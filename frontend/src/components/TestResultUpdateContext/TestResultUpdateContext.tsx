import React from "react";
interface Context {
  update: (id: number) => void;
}
export const TestResultUpdateContext = React.createContext<Context>({
  update: () => {},
});
