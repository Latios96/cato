import React from "react";
import Header from "../components/Header/Header";
import Footer from "../components/Footer/Footer";
import { Helmet } from "react-helmet";

interface Props {
  title?: string;
}

const BasicPage: React.FunctionComponent<Props> = (props) => {
  return (
    <>
      <div style={{ minHeight: "100vh" }}>
        <Header />
        {props.children}
      </div>
      <Footer />
    </>
  );
};

export default BasicPage;
