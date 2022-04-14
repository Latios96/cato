import React, { PropsWithChildren } from "react";
import Header from "../components/Header/Header";
import Footer from "../components/Footer/Footer";
import { Helmet } from "react-helmet";

interface Props {
  title?: string;
}

const BasicPage = (props: PropsWithChildren<Props>) => {
  return (
    <>
      <Helmet>
        <title>{props.title || "Cato"}</title>
      </Helmet>
      <div style={{ minHeight: "100vh" }}>
        <Header />
        {props.children}
      </div>
      <Footer />
    </>
  );
};

export default BasicPage;
