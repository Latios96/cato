import React from "react";
import Header from "../components/Header/Header";

interface Props {}

const BasicPage: React.FunctionComponent<Props> = (props) => {
  return (
    <div>
      <Header />
      {props.children}
    </div>
  );
};

export default BasicPage;
