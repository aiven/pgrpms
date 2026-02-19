#!/usr/bin/bash
# aws_sync_config.sh — Shared configuration for aws_sync scripts.
# Source this file from other scripts: source "$(dirname "$0")/aws_sync_config.sh"

VALID_ARCH=("aarch64" "ppc64le" "x86_64")

# Usage: is_valid <value> <array_element>...
# Example: is_valid "$arch" "${VALID_ARCH[@]}"
is_valid() {
  local val="$1"; shift
  local item
  for item in "$@"; do
    [[ "$item" == "$val" ]] && return 0
  done
  return 1
}
VALID_PG_VERSIONS=(13 14 15 16 17 18)
VALID_REDHAT_OS_VERSIONS=(7 8.10 9.6 9.7 10.0 10.1)
VALID_FEDORA_OS_VERSIONS=(41 42 43)
