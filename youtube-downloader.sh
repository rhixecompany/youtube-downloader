#!/usr/bin/env bash
# YouTube CLI wrapper — interactive by default; non-interactive with --non-interactive
# Example interactive: ./youtube-downloader.sh
# Example non-interactive: ./youtube-downloader.sh "https://youtube.com/watch?v=xxx"

set -euo pipefail
cd "$(dirname "$0")"

# Activate project virtualenv (myvenv)
if [ ! -f ./myvenv/Scripts/activate ]; then
  echo "ERROR: virtualenv not found. Run: python -m venv myvenv" >&2
  exit 1
fi
# shellcheck disable=SC1091
source ./myvenv/Scripts/activate

# Default to interactive mode; --non-interactive skips prompt
INTERACTIVE=1
ARGS=()

for arg in "$@"; do
  if [ "$arg" = "--non-interactive" ]; then
    INTERACTIVE=0
  else
    ARGS+=("$arg")
  fi
done

if [ ${#ARGS[@]} -gt 0 ]; then
  # Non-interactive: pass URL directly
  echo "Running in non-interactive mode with URL: ${ARGS[0]}"
  python main_noplaylist.py "${ARGS[0]}"
else
  # Interactive mode: ask user for URL
  echo "Running in interactive mode (default)."
  echo "Enter a video URL (or pass --non-interactive <url> to skip this prompt):"
  echo -n "URL: "
  read -r url
  if [ -z "$url" ]; then
    echo "No URL entered. Exiting."
    exit 1
  fi
  python main_noplaylist.py "$url"
fi