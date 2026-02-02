#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate

if pytest; then
  exit 0
else
  exit 1
fi
