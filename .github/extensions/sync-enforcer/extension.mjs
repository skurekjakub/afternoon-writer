import { joinSession } from "@github/copilot-sdk/extension";

const SYNC_REMINDER = [
  "CRITICAL DISPATCH RULE: Every `task` tool call MUST use mode: \"sync\" (or omit mode entirely).",
  "NEVER set mode to \"background\". NEVER use background agents.",
  "If you are the afternoon-orchestrator: you dispatch, you WAIT for the return, you read status.json.",
  "No polling. No read_agent. No background. Synchronous only.",
].join(" ");

const FILE_WRITE_REMINDER =
  "MANDATORY: You have full file-write access via create and edit tools. " +
  "Your task requires writing output files. Do NOT end your turn without writing all required artifacts. " +
  "If your task says to produce a file (v1.md, v2.md, v2g.md, v3.md, v4.md, v4b.md, status.json, etc.), " +
  "you MUST write it before finishing. Use the create or edit tool now.";

// Track tool calls per turn to inject periodic file-write reminders
let toolCallCount = 0;
const FILE_WRITE_REMINDER_INTERVAL = 8;

// Tools that suggest the agent is reading/researching but may forget to write
const READ_TOOLS = new Set(["view", "glob", "grep", "rg", "web_fetch", "skill"]);

// Tools that indicate the agent IS writing (reset reminder counter)
const WRITE_TOOLS = new Set(["edit", "create", "apply_patch"]);

const session = await joinSession({
  tools: [],
  hooks: {
    // Inject sync-mode reminder at session start
    onSessionStart: async (input) => {
      return {
        additionalContext: SYNC_REMINDER,
        suppressOutput: true,
      };
    },

    // Inject sync-mode reminder on every user/orchestrator prompt
    onUserPromptSubmitted: async (input) => {
      toolCallCount = 0; // reset per-turn counter
      return {
        additionalContext: SYNC_REMINDER,
        suppressOutput: true,
      };
    },

    // INTERCEPT tool calls
    onPreToolUse: async (input) => {
      // --- TASK TOOL: force sync mode ---
      if (input.toolName === "task") {
        const args = input.toolArgs || {};
        const mode = String(args.mode || "").toLowerCase();

        if (mode === "background" || mode === "async") {
          const fixed = { ...args, mode: "sync" };
          delete fixed.background;
          await session.log(
            `[sync-enforcer] BLOCKED background dispatch of "${args.agent_type || args.name || "unknown"}". Forced to sync.`,
            { level: "warning" }
          );
          return {
            modifiedArgs: fixed,
            additionalContext:
              "SYNC ENFORCER: Your dispatch was rewritten from background to sync. " +
              "You MUST NOT use background mode. Wait for the synchronous return. " +
              "Do NOT call read_agent or list_agents — the result is already in the task return value.",
            permissionDecision: "allow",
            suppressOutput: false,
          };
        }

        return {
          permissionDecision: "allow",
          suppressOutput: true,
        };
      }

      // --- BLOCK background agent tools ---
      if (input.toolName === "read_agent" || input.toolName === "list_agents") {
        await session.log(
          `[sync-enforcer] BLOCKED ${input.toolName}. Use synchronous task dispatch instead.`,
          { level: "warning" }
        );
        return {
          permissionDecision: "deny",
          permissionDecisionReason:
            "Background agent polling is forbidden. All task dispatches must be synchronous (mode: \"sync\"). " +
            "The task tool blocks until the agent finishes and returns the result directly. " +
            "Do NOT use read_agent. Re-dispatch with mode: \"sync\".",
          suppressOutput: false,
        };
      }

      if (input.toolName === "write_agent") {
        await session.log(
          `[sync-enforcer] BLOCKED write_agent. No background agents allowed.`,
          { level: "warning" }
        );
        return {
          permissionDecision: "deny",
          permissionDecisionReason:
            "Background agent interaction is forbidden. All dispatches must be synchronous.",
          suppressOutput: false,
        };
      }
    },

    // After tool calls: reinforce rules + file-write reminders
    onPostToolUse: async (input) => {
      // After task dispatch, reinforce sync rule
      if (input.toolName === "task") {
        return {
          additionalContext:
            "The task returned synchronously. Read the agent's status.json now and route to the next step. " +
            "Do NOT call read_agent. Do NOT use background mode on the next dispatch.",
          suppressOutput: true,
        };
      }

      // Track tool calls for file-write reminder injection
      if (WRITE_TOOLS.has(input.toolName)) {
        toolCallCount = 0; // agent is writing, reset counter
        return { suppressOutput: true };
      }

      if (READ_TOOLS.has(input.toolName)) {
        toolCallCount++;

        // Every N read-type tool calls without a write, inject a reminder
        if (toolCallCount > 0 && toolCallCount % FILE_WRITE_REMINDER_INTERVAL === 0) {
          await session.log(
            `[sync-enforcer] ${toolCallCount} tool calls without a file write. Injecting reminder.`,
            { level: "warning" }
          );
          return {
            additionalContext: FILE_WRITE_REMINDER,
            suppressOutput: false,
          };
        }
      }

      return { suppressOutput: true };
    },
  },
});

await session.log("[sync-enforcer] Extension loaded. Sync enforcement + file-write reminders active.");
