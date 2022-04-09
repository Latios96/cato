import React, { PropsWithChildren } from "react";
import Header from "../components/Header/Header";
import Footer from "../components/Footer/Footer";

interface Props {
  title?: string;
}

const BasicPage = (props: PropsWithChildren<Props>) => {
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
