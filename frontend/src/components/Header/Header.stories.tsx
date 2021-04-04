import { Meta } from "@storybook/react";
import Header from "./Header";
import React from "react";
import { HashRouter } from "react-router-dom";

export default {
  title: "Header",
  component: Header,
} as Meta;

export const Default: React.VFC<{}> = () => (
  <HashRouter>
    <Header />
  </HashRouter>
);
