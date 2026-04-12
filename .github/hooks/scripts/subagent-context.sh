#!/usr/bin/env bash
# Injected into every subagent at spawn time.
# Eliminates the "conflicting instructions / no file tools" reasoning loop
# that GPT 5.4 enters when the subagent context priors suggest restricted tool access.
# Also enforces sync-only dispatch and mandatory file writes.
echo "You have full tool access: bash, view, create, edit, grep, glob, web_fetch, task, skill. \
Write output files directly — do not debate tool availability. \
If your task produces a file artifact, create or edit it with the provided tools. \
There is no restriction on file writes. \
FILE WRITING IS MANDATORY: If your task specifies an output file, you MUST write it using create or edit before finishing. \
Do not end your turn without writing all required files. Do not announce what you would write — actually write it. \
CRITICAL: If you use the task tool, you MUST use mode: sync. NEVER use mode: background. \
All dispatches are synchronous — the task call blocks until the agent finishes. \
Do not use read_agent, write_agent, or list_agents. These are forbidden."
