import { setTimeout as delay } from "node:timers/promises";
import { joinSession } from "@github/copilot-sdk/extension";

const MAX_SECONDS = 86400;

// Active abort controllers keyed by toolCallId — lets subagent events wake sleeps.
const activeSleeps = new Map();

// session.log can throw ERR_STREAM_DESTROYED if the stdio pipe is already torn
// down during extension reload. Swallow only that specific error.
async function safeLog(msg, opts) {
  try {
    await session.log(msg, opts);
  } catch (err) {
    if (err?.code !== "ERR_STREAM_DESTROYED") throw err;
  }
}

function parseSeconds(args) {
  if (typeof args === "number") {
    return args;
  }

  if (typeof args === "string" && args.trim() !== "") {
    return Number(args.trim());
  }

  if (args && typeof args === "object") {
    const value = args.seconds ?? args.duration ?? args.value;
    if (typeof value === "number") {
      return value;
    }

    if (typeof value === "string" && value.trim() !== "") {
      return Number(value.trim());
    }
  }

  return Number.NaN;
}

const session = await joinSession({
  tools: [
    {
      name: "sleep",
      description:
        "Pause execution for the given number of seconds. Wakes early if a subagent completes before the timer expires. Use when you need to wait before polling a long-running process. Example: sleep({ seconds: 1200 }).",
      skipPermission: true,
      parameters: {
        type: "object",
        properties: {
          seconds: {
            type: "integer",
            minimum: 1,
            maximum: MAX_SECONDS,
            description: "Duration to sleep in whole seconds. Example: 1200",
          },
        },
        required: ["seconds"],
      },
      handler: async (args, invocation) => {
        const seconds = parseSeconds(args);

        if (!Number.isInteger(seconds) || seconds < 0 || seconds > MAX_SECONDS) {
          return {
            textResultForLlm:
              "Invalid sleep duration. Provide a whole number of seconds between 0 and 86400.",
            resultType: "failure",
            error: "seconds must be an integer between 0 and 86400",
          };
        }

        const ac = new AbortController();
        const startMs = Date.now();
        activeSleeps.set(invocation.toolCallId, ac);

        await safeLog(
          `sleep(${seconds}) started for tool call ${invocation.toolCallId}`,
          { level: "info", ephemeral: true },
        );

        let wokeEarly = false;
        try {
          await delay(seconds * 1000, undefined, { signal: ac.signal });
        } catch (err) {
          if (err.name === "AbortError") {
            wokeEarly = true;
          } else {
            throw err;
          }
        } finally {
          activeSleeps.delete(invocation.toolCallId);
        }

        const elapsed = Math.round((Date.now() - startMs) / 1000);

        if (wokeEarly) {
          await safeLog(
            `sleep woke early after ${elapsed}s (subagent completed)`,
            { level: "info", ephemeral: true },
          );
          return `Woke early after ${elapsed} second${elapsed === 1 ? "" : "s"} — a subagent completed.`;
        }

        await safeLog(`sleep(${seconds}) finished`, {
          level: "info",
          ephemeral: true,
        });

        return `Slept for ${seconds} second${seconds === 1 ? "" : "s"}.`;
      },
    },
  ],
});

// Wake all active sleeps when any subagent finishes.
session.on("subagent.completed", () => {
  for (const [id, ac] of activeSleeps) {
    ac.abort();
  }
});

session.on("session.shutdown", () => {
  // Cancel any lingering sleeps so the process can exit cleanly.
  // Don't log here — the stdio stream may already be destroyed.
  for (const [, ac] of activeSleeps) {
    ac.abort();
  }
});