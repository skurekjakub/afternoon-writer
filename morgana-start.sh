#!/usr/bin/env bash
set -uo pipefail

# --- Env vars for long autonomous runs ---
export COPILOT_TASK_WAIT_TIMEOUT_SECONDS=360000
export CONFIGURE_COPILOT_AGENT=false
export COPILOT_SWE_AGENT_BACKGROUND_AGENTS=true
export COPILOT_SWE_AGENT_PARALLEL_TASK_EXECUTION=true
export COPILOT_LARGE_OUTPUT_MAX_BYTES=104857600
export COPILOT_BUFFER_EXHAUSTION_THRESHOLD=0.99
export COPILOT_LARGE_OUTPUT_THRESHOLD_BYTES=204800

DONE_MARKER="===MORGANA DONE==="
AGENT_NAME="outliner-morgana-orchestrator"
AGENT_FILE="./.github/agents/${AGENT_NAME}.agent.md"

# --- Story directory (required argument) ---
STORY_DIR="${1:-}"
if [[ -z "$STORY_DIR" ]]; then
  echo "Usage: $0 <story-directory>"
  echo "  e.g., $0 stories/ravencrest"
  exit 1
fi

# --- Pre-flight ---
if [[ ! -f "$AGENT_FILE" ]]; then
  echo "ERROR: Agent file not found: ${AGENT_FILE}" >&2
  exit 1
fi

if ! grep -qF "$DONE_MARKER" "$AGENT_FILE"; then
  echo "ERROR: Stop marker '${DONE_MARKER}' not found in ${AGENT_FILE}" >&2
  exit 1
fi

if [[ ! -d "$STORY_DIR" ]]; then
  echo "ERROR: Story directory not found: ${STORY_DIR}" >&2
  exit 1
fi

BRIEF="${STORY_DIR}/.morgana/brief.md"
if [[ ! -f "$BRIEF" ]]; then
  echo "ERROR: Brief not found at ${BRIEF}" >&2
  echo "Create the brief first, then re-run." >&2
  exit 1
fi

echo "[$(date)] Pre-flight OK: agent '${AGENT_NAME}' validated, story dir '${STORY_DIR}', brief exists."
mkdir -p logs/morgana

while true; do
  TIMESTAMP=$(date +%s)
  LOG_DIR="./logs/morgana"
  LOG_FILE="${LOG_DIR}/copilot_${TIMESTAMP}.log"
  SHARE_FILE="${LOG_DIR}/share_${TIMESTAMP}.md"

  echo "[$(date)] Starting copilot run (log: ${LOG_FILE})"

  copilot \
    --yolo \
    --agent "${AGENT_NAME}" \
    --log-level "debug" \
    --log-dir "${LOG_DIR}/" \
    --share "${SHARE_FILE}" \
    --experimental \
    --reasoning-effort xhigh \
    -p "Story directory: ${STORY_DIR}" 2>&1 | tee "${LOG_FILE}"

  EXIT_CODE=${PIPESTATUS[0]}

  # --- Check for done marker in output ---
  if grep -qF "${DONE_MARKER}" "${LOG_FILE}"; then
    echo "[$(date)] Found '${DONE_MARKER}' in output. Morgana has finished weaving."
    exit 0
  fi

  if [[ ${EXIT_CODE} -ne 0 ]]; then
    echo "[$(date)] Copilot exited with code ${EXIT_CODE}. Restarting in 5s..."
    sleep 5
  else
    echo "[$(date)] Copilot exited cleanly without done marker. Restarting in 2s..."
    sleep 2
  fi
done
