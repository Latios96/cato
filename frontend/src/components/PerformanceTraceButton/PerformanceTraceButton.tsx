import { Speedometer2 } from "react-bootstrap-icons";
import Button from "../Button/Button";
import { PropsWithChildren } from "react";

interface Props {
  runId: number;
  performanceTraceId?: number;
  disabled?: boolean;
}
const ORIGIN = "https://ui.perfetto.dev";

function openTrace(arrayBuffer: any, traceUrl: string, title: string) {
  const win = window.open(ORIGIN);
  if (!win) {
    // eslint-disable-next-line no-console
    console.log(`Popups blocked, you need to manually click the button`);
    return;
  }

  const timer = setInterval(() => win.postMessage("PING", ORIGIN), 50);

  const onMessageHandler = (evt: any) => {
    if (evt.data !== "PONG") return;

    window.clearInterval(timer);
    window.removeEventListener("message", onMessageHandler);

    // eslint-disable-next-line no-restricted-globals
    const reopenUrl = new URL(location.href);
    reopenUrl.hash = `#reopen=${traceUrl}`;
    win.postMessage(
      {
        perfetto: {
          buffer: arrayBuffer,
          title: title,
          url: reopenUrl.toString(),
        },
      },
      ORIGIN
    );
  };

  window.addEventListener("message", onMessageHandler);
}

async function fetchAndOpen(runId: number) {
  const traceUrl = `/api/v1/runs/${runId}/performance_trace`;
  const resp = await fetch(traceUrl);
  if (!resp.ok) {
    return;
  }
  const blob = await resp.blob();

  const arrayBuffer = await blob.arrayBuffer();
  openTrace(arrayBuffer, traceUrl, `Cato Run #${runId}`);
}

const PerformanceTraceButton = (props: PropsWithChildren<Props>) => {
  return (
    <>
      <Button
        onClick={() => fetchAndOpen(props.runId)}
        disabled={props.performanceTraceId == null}
      >
        {props.children}
      </Button>
    </>
  );
};

export default PerformanceTraceButton;
