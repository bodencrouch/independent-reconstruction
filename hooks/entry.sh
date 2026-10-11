#!/bin/sh
# Keep an inactive project neutral without importing Python or private policy.
# This bootstrap is not an isolation boundary and never sets run/role itself.
host=${1-}
event=${2-}
case "$host" in
  cursor|claude|codex) ;;
  *) printf '%s\n' '{"error":"Unsupported hook host"}'; exit 2 ;;
esac
if [ -z "${IR_RUN-}" ] && [ -z "${IR_ROLE-}" ]; then
  if [ "$host" = cursor ]; then
    case "$event" in
      preToolUse|beforeShellExecution|beforeMCPExecution|beforeReadFile|beforeTabFileRead|subagentStart)
        printf '%s\n' '{"permission":"allow"}' ;;
      beforeSubmitPrompt) printf '%s\n' '{"continue":true}' ;;
      *) printf '%s\n' '{}' ;;
    esac
  else
    printf '%s\n' '{}'
  fi
  exit 0
fi
hook_dir=${0%/*}
exec python3 "$hook_dir/$host.py" --event "$event"
