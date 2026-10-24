import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

// Separate from Herdr's managed integration so its updates preserve this hook.
export default function (pi: ExtensionAPI) {
  const pane = process.env.HERDR_PANE_ID;
  if (process.env.HERDR_ENV !== "1" || !pane) return;

  let timer: ReturnType<typeof setInterval> | undefined;
  let lastSnapshot: string | undefined;
  let subagentCount = 0;
  let busy = false;
  let stopped = true;

  // pi-subagents emits this from its reconciled active-run projection,
  // including restored runs and foreground workflows.
  const unsubscribe = pi.events.on("herdr:busy", (data: unknown) => {
    if (typeof data !== "object" || data === null || !("active" in data)) return;
    if (data.active === false) {
      subagentCount = 0;
    } else if (data.active === true && "label" in data && typeof data.label === "string") {
      const match = /^⏳ (\d+) subagents?\b/u.exec(data.label);
      if (match) subagentCount = Number(match[1]);
    }
    // Publish on the timer so a false/true label refresh stays atomic.
  });

  async function publish() {
    if (stopped || busy) return;
    const name = pi.getSessionName()?.trim() || "Unnamed session";
    const badge = subagentCount > 0 ? `${subagentCount} 👾` : "";
    const snapshot = JSON.stringify([name, badge]);
    if (snapshot === lastSnapshot) return;
    busy = true;
    try {
      const result = await pi.exec("herdr", [
        "pane", "report-metadata", pane,
        "--source", "pi-session-label", "--agent", "pi",
        "--applies-to-source", "herdr:pi",
        "--token", `session_name=${name}`,
        ...(badge ? ["--token", `subagents=${badge}`] : ["--clear-token", "subagents"]),
      ], { timeout: 2000 });
      if (result.code === 0) lastSnapshot = snapshot;
    } catch {
      // Retry on the next tick if Herdr is temporarily unavailable.
    } finally {
      busy = false;
    }
  }

  pi.on("session_start", async (_event, ctx) => {
    if (ctx.mode !== "tui") return;
    stopped = false;
    lastSnapshot = undefined;
    await publish();
    // Also tracks /name changes while the agent is idle.
    timer = setInterval(() => { void publish(); }, 2000);
    timer.unref();
  });
  pi.on("session_shutdown", () => {
    stopped = true;
    unsubscribe();
    if (timer) clearInterval(timer);
    timer = undefined;
  });
}
