#!/usr/bin/env bash
# Run all snapshots for the day's cron cycle.
# Failures on one network don't abort the others.

set -u
cd "$(dirname "$0")/.."

PY=.venv/bin/python
TS="$(date -u +%FT%TZ)"

echo "[$TS] --- snapshot run start ---"

$PY -m gecko.snapshot --network solana --kind trending || echo "[$TS] FAILED: solana trending"
$PY -m gecko.snapshot --network solana --kind new      || echo "[$TS] FAILED: solana new"
$PY -m gecko.snapshot --network base   --kind new      || echo "[$TS] FAILED: base new"

echo "[$TS] --- snapshot run end ---"
