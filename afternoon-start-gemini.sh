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
#   AFTERNOON_MODEL             Override the session model slug (run `agy models`
#                               to see available Gemini slugs). When unset, uses
#                               agy defaults and per-agent `pro`/`flash` tiers.
#   AFTERNOON_EFFORT            Reasoning effort: low | medium | high | xhigh | max
#                               (default: high).
#   AFTERNOON_SKIP_PERMISSIONS  Pass --dangerously-skip-permissions for headless
#                               autonomous runs (default: true). Set to "false"
#                               if you prefer scoped settings.json allow rules.
#   AFTERNOON_MODE              Optional --mode override (e.g., accept-edits).
#                               Left unset by default because `--mode auto` is
#                               not available on all account tiers.
#
# Usage:
#   ./afternoon-start-gemini.sh
#   AFTERNOON_EFFORT=xhigh ./afternoon-start-gemini.sh
#   AFTERNOON_MODEL=<slug> ./afternoon-start-gemini.sh
# =============================================================================

AFTERNOON_EFFORT="${AFTERNOON_EFFORT:-high}"
AFTERNOON_SKIP_PERMISSIONS="${AFTERNOON_SKIP_PERMISSIONS:-true}"
AFTERNOON_MODE="${AFTERNOON_MODE:-}"
AFTERNOON_MODEL="${AFTERNOON_MODEL:-}"

DONE_MARKER="===AFTERNOON DONE==="
AGENT_NAME="afternoon-orchestrator"
AGENT_FILE="./.agents/agents/${AGENT_NAME}.md"
SKILLS_FILE="./.agents/skills.json"
SCHEMA_FILE="./.agents/schemas/orchestrator-result.schema.json"

# --- Pre-flight checks ---
if ! command -v agy >/dev/null 2>&1; then
  echo "ERROR: 'agy' (Antigravity CLI) not found on PATH." >&2
  echo "  Install Antigravity CLI and authenticate interactively once with 'agy'." >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: 'python3' not found on PATH (needed to validate JSON output)." >&2
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

if [[ ! -f "${SCHEMA_FILE}" ]]; then
  echo "ERROR: Output schema not found: ${SCHEMA_FILE}" >&2
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
PERM_DESC="skip-permissions=${AFTERNOON_SKIP_PERMISSIONS}"
if [[ -n "${AFTERNOON_MODE}" ]]; then
  PERM_DESC="${PERM_DESC}, mode=${AFTERNOON_MODE}"
fi
echo "[$(date)] Antigravity CLI (agy) | ${PERM_DESC} | effort=${AFTERNOON_EFFORT} | model=${MODEL_DESC}"
echo "[$(date)] Pre-flight OK: agent '${AGENT_NAME}', skills, schema, config, and ${BEAT_COUNT} outline file(s) validated."

mkdir -p logs/afternoon

validate_and_route() {
  local json_file="$1"
  local schema_file="$2"
  python3 - "$json_file" "$schema_file" <<'PY'
import json
import sys

json_path, schema_path = sys.argv[1], sys.argv[2]

try:
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)
except Exception as exc:
    print(f"SCHEMA_ERROR: Could not read schema: {exc}", file=sys.stderr)
    sys.exit(3)

try:
    with open(json_path, encoding="utf-8") as f:
        raw = f.read().strip()
except OSError as exc:
    print(f"INVALID_OUTPUT: Could not read output file: {exc}", file=sys.stderr)
    sys.exit(2)

if not raw:
    print("INVALID_OUTPUT: Empty stdout from agy", file=sys.stderr)
    sys.exit(2)

try:
    envelope = json.loads(raw)
except json.JSONDecodeError as exc:
    print(f"INVALID_OUTPUT: Output is not valid JSON: {exc}", file=sys.stderr)
    sys.exit(2)

payload = envelope
if isinstance(envelope, dict) and "structured_output" in envelope and isinstance(envelope["structured_output"], dict):
    payload = envelope["structured_output"]
elif isinstance(envelope, dict) and "result" in envelope and isinstance(envelope["result"], str):
    try:
        parsed = json.loads(envelope["result"])
        if isinstance(parsed, dict):
            payload = parsed
    except json.JSONDecodeError:
        pass

if not isinstance(payload, dict):
    print("SCHEMA_MISMATCH: Payload is not a JSON object", file=sys.stderr)
    sys.exit(2)

required = schema.get("required", [])
props = schema.get("properties", {})
errors = []

for key in required:
    if key not in payload:
        errors.append(f"missing required field '{key}'")

if schema.get("additionalProperties") is False:
    extra = set(payload.keys()) - set(props.keys())
    if extra:
        errors.append(f"unexpected field(s): {sorted(extra)}")

type_checks = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
    "boolean": lambda v: isinstance(v, bool),
}

for key, spec in props.items():
    if key not in payload:
        continue
    val = payload[key]
    expected_type = spec.get("type")
    if expected_type in type_checks and not type_checks[expected_type](val):
        errors.append(f"field '{key}' expected {expected_type}, got {type(val).__name__}")
        continue
    if "enum" in spec and val not in spec["enum"]:
        errors.append(f"field '{key}' value {val!r} not in {spec['enum']}")
    if expected_type == "integer" and "minimum" in spec and val < spec["minimum"]:
        errors.append(f"field '{key}' value {val} < minimum {spec['minimum']}")
    if expected_type == "array" and "items" in spec:
        item_type = spec["items"].get("type")
        if item_type in type_checks:
            for idx, item in enumerate(val):
                if not type_checks[item_type](item):
                    errors.append(f"field '{key}[{idx}]' expected {item_type}, got {type(item).__name__}")

if errors:
    print("SCHEMA_MISMATCH: " + "; ".join(errors), file=sys.stderr)
    sys.exit(2)

status = payload["status"]
marker = payload["completionMarker"]
completed = payload["chaptersCompleted"]
total = payload["chaptersTotal"]
blocked = payload["blockedChapters"]
summary = payload["summary"]

print(f"VALID_JSON status={status} progress={completed}/{total} blocked={len(blocked)} marker={marker!r}")
print(f"SUMMARY: {summary}")

if status in ("completed", "completed-with-blocks", "flagged") and marker == "===AFTERNOON DONE===":
    sys.exit(0)
if status == "error":
    sys.exit(3)
# status == "in-progress" or missing marker -> restart loop
sys.exit(2)
PY
}

while true; do
  TIMESTAMP=$(date +%s)
  LOG_DIR="./logs/afternoon"
  OUT_FILE="${LOG_DIR}/agy_gemini_${TIMESTAMP}.json"
  ERR_FILE="${LOG_DIR}/agy_gemini_${TIMESTAMP}.stderr.log"

  AGY_ARGS=(
    --agent "${AGENT_NAME}"
    --effort "${AFTERNOON_EFFORT}"
    --output-format json
    --json-schema "${SCHEMA_FILE}"
  )

  if [[ "${AFTERNOON_SKIP_PERMISSIONS}" == "true" ]]; then
    AGY_ARGS+=(--dangerously-skip-permissions)
  fi

  if [[ -n "${AFTERNOON_MODE}" ]]; then
    AGY_ARGS+=(--mode "${AFTERNOON_MODE}")
  fi

  if [[ -n "${AFTERNOON_MODEL}" ]]; then
    AGY_ARGS+=(--model "${AFTERNOON_MODEL}")
  fi

  AGY_ARGS+=(-p "begin")

  echo "[$(date)] Starting agy run (stdout: ${OUT_FILE}, stderr: ${ERR_FILE})"

  agy "${AGY_ARGS[@]}" > "${OUT_FILE}" 2> >(tee "${ERR_FILE}" >&2)
  EXIT_CODE=$?

  validate_and_route "${OUT_FILE}" "${SCHEMA_FILE}"
  ROUTE_CODE=$?

  if [[ ${ROUTE_CODE} -eq 0 ]]; then
    echo "[$(date)] Verified schema output: pipeline finished cleanly."
    exit 0
  elif [[ ${ROUTE_CODE} -eq 3 ]]; then
    echo "[$(date)] Pipeline reported fatal error (see ${OUT_FILE} and ${ERR_FILE}). Stopping." >&2
    exit 1
  fi

  if [[ ${EXIT_CODE} -ne 0 ]]; then
    echo "[$(date)] agy exited with code ${EXIT_CODE} (output not complete). Restarting in 5s..."
    sleep 5
  else
    echo "[$(date)] agy exited without terminal completion status. Restarting in 2s..."
    sleep 2
  fi
done
