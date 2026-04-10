#!/usr/bin/env bash
# Injected into every subagent at spawn time.
# Eliminates the "conflicting instructions / no file tools" reasoning loop
# that GPT 5.4 enters when the subagent context priors suggest restricted tool access.
echo "You have full tool access: bash, view, create, edit, grep, glob, web_fetch, task, skill. \
Write output files directly — do not debate tool availability. \
If your task produces a file artifact, create or edit it with the provided tools. \
There is no restriction on file writes."
