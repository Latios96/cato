import React from "react";
import style from "./LogComponent.module.css";
interface Props {
  content: string;
}
const LogComponent = (props: Props) => {
  return (
    <div>
      <div className={style.terminalBackground}>
        <pre className={style.terminalContent}>
          <code>{props.content}</code>
        </pre>
      </div>
    </div>
  );
};

export default LogComponent;
