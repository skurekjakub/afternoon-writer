#!/usr/bin/env bash
set -uo pipefail

# =============================================================================
# afternoon-start-gemini.sh — afternoon pipeline on Gemini via Antigravity CLI
#
# Prerequisites:
#   1. Antigravity CLI (`agy`) installed and on PATH.
#   2. Authenticated interactively once (run `agy` and complete sign-in).
#   3. Project configured at `.afternoon/config.json` with outlines in
#      `.afternoon/outlines/*.md`.
#
# Optional Environment Variables:
#   AFTERNOON_MODEL   Override the session model slug (run `agy models` to see
#                     available Gemini slugs). When unset, uses agy defaults
#                     and per-agent `pro`/`flash` model tiers.
#   AFTERNOON_EFFORT  Reasoning effort: low | medium | high | xhigh | max
#                     (default: high).
#   AFTERNOON_MODE    Execution mode: auto | accept-edits | plan
#                     (default: auto — auto-approves workspace edits and
#                     sandboxed commands).
#
# Usage:
#   ./afternoon-start-gemini.sh
#   AFTERNOON_EFFORT=xhigh ./afternoon-start-gemini.sh
#   AFTERNOON_MODEL=<slug> ./afternoon-start-gemini.sh
# =============================================================================

AFTERNOON_EFFORT="${AFTERNOON_EFFORT:-high}"
AFTERNOON_MODE="${AFTERNOON_MODE:-auto}"
AFTERNOON_MODEL="${AFTERNOON_MODEL:-}"

DONE_MARKER="===AFTERNOON DONE==="
AGENT_NAME="afternoon-orchestrator"
AGENT_FILE="./.agents/agents/${AGENT_NAME}.md"
SKILLS_FILE="./.agents/skills.json"

# --- Pre-flight checks ---
if ! command -v agy >/dev/null 2>&1; then
  echo "ERROR: 'agy' (Antigravity CLI) not found on PATH." >&2
  echo "  Install Antigravity CLI and authenticate interactively once with 'agy'." >&2
  exit 1
fi

if [[ ! -f "${AGENT_FILE}" ]]; then
  echo "ERROR: Agent file not found: ${AGENT_FILE}" >&2
  exit 1
fi

if ! grep -qF "${DONE_MARKER}" "${AGENT_FILE}"; then
  echo "ERROR: Stop marker '${DONE_MARKER}' not found in ${AGENT_FILE}" >&2
  exit 1
fi

if [[ ! -f "${SKILLS_FILE}" ]]; then
  echo "ERROR: Skills config not found: ${SKILLS_FILE}" >&2
  exit 1
fi

if [[ ! -f ".afternoon/config.json" ]]; then
  echo "ERROR: No config found at .afternoon/config.json" >&2
  exit 1
fi

if [[ ! -d ".afternoon/outlines" ]]; then
  echo "ERROR: No outlines directory at .afternoon/outlines/" >&2
  exit 1
fi

BEAT_COUNT=$(find .afternoon/outlines/ -name "*.md" | wc -l)
if [[ ${BEAT_COUNT} -eq 0 ]]; then
  echo "ERROR: No outline files found in .afternoon/outlines/" >&2
  exit 1
fi

MODEL_DESC="${AFTERNOON_MODEL:-default (per-agent pro/flash tiers)}"
echo "[$(date)] Antigravity CLI (agy) | mode=${AFTERNOON_MODE} | effort=${AFTERNOON_EFFORT} | model=${MODEL_DESC}"
echo "[$(date)] Pre-flight OK: agent '${AGENT_NAME}' validated, skills registered, config exists, ${BEAT_COUNT} outline file(s) found."

mkdir -p logs/afternoon

while true; do
  TIMESTAMP=$(date +%s)
  LOG_DIR="./logs/afternoon"
  LOG_FILE="${LOG_DIR}/agy_gemini_${TIMESTAMP}.log"

  AGY_ARGS=(
    --agent "${AGENT_NAME}"
    --mode "${AFTERNOON_MODE}"
    --effort "${AFTERNOON_EFFORT}"
  )

  if [[ -n "${AFTERNOON_MODEL}" ]]; then
    AGY_ARGS+=(--model "${AFTERNOON_MODEL}")
  fi

  AGY_ARGS+=(-p "begin")

  echo "[$(date)] Starting agy run (log: ${LOG_FILE})"

  agy "${AGY_ARGS[@]}" 2>&1 | tee "${LOG_FILE}"
  EXIT_CODE=${PIPESTATUS[0]}

  # --- Check for done marker in output ---
  if grep -qF "${DONE_MARKER}" "${LOG_FILE}"; then
    echo "[$(date)] Found '${DONE_MARKER}' in output. Pipeline complete."
    exit 0
  fi

  if [[ ${EXIT_CODE} -ne 0 ]]; then
    echo "[$(date)] agy exited with code ${EXIT_CODE}. Restarting in 5s..."
    sleep 5
  else
    echo "[$(date)] agy exited cleanly without done marker. Restarting in 2s..."
    sleep 2
  fi
done
