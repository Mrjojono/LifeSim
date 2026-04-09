#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PDDL_DIR="$ROOT_DIR/pddl"

rm -f "$PDDL_DIR"/problem_cleaner_*.pddl
rm -f "$ROOT_DIR"/sas_plan "$ROOT_DIR"/sas_plan.*
rm -f "$ROOT_DIR"/output.sas

echo "Fichiers générés supprimés."
