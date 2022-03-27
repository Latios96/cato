import React from "react";
import styles from "./Footer.module.scss";
import { CachePolicies, useFetch } from "use-http";

interface AboutInformation {
  version: string;
}
function Footer() {
  const { data } = useFetch<AboutInformation>(
    `/api/v1/about`,
    { cachePolicy: CachePolicies.CACHE_FIRST },
    []
  );
  return (
    <div className={styles.footer}>
      <div>
        <span>Cato</span>
        <span>Build info: {data?.version}</span>
      </div>
    </div>
  );
}

export default Footer;
