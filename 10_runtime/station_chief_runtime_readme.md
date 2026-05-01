# Station Chief Runtime Skeleton

## Status
Initial runnable runtime skeleton upgraded to v0.2.0. Locked 175-family baseline preserved.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, optionally writes runtime artifacts, and returns deterministic demo output.

## What This Does
- Loads Family 7 and Devinization Packs 1 through 7
- Confirms overlays exist
- Preserves baseline architecture
- Supports one-command intake
- Supports command classification
- Supports activation-tier selection
- Selects relevant overlays
- Creates command briefs
- Creates non-executing work orders
- Produces deterministic JSON output
- Writes optional runtime artifacts
- Runs deterministic fixture tests
- Supports check please, blueberry pancakes, Square Block Square Hole, Speed Racer, build, route, repair, governance, and final output command types

## What This Does Not Do
- Does not modify baseline family files
- Does not regenerate exports
- Does not connect live APIs
- Does not animate all 47,250 worker agents
- Does not execute work orders yet
- Does not build UI yet
- Does not claim production readiness

## Commands
python3 10_runtime/station_chief_runtime.py --demo

python3 10_runtime/station_chief_runtime.py --command "check please" --json

python3 10_runtime/station_chief_runtime.py --command "build Station Chief runtime skeleton" --brief

python3 10_runtime/station_chief_runtime.py --list-overlays

python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs

python3 10_runtime/station_chief_runtime.py --fixture-test

python3 10_runtime/station_chief_fixture_tests.py

## Runtime Artifacts
When `--write-artifacts` is used, the runtime creates a deterministic run directory containing:
- run_log.json
- command_brief.json
- work_orders.json
- selected_overlays.json
- evidence.json
- manifest.json
- full_result.json

## Runtime Doctrine
The Station Chief runtime skeleton keeps the full 175-family command civilization intact while activating only the logic needed for a specific task. This skeleton proves command intake, classification, overlay loading, activation-tier selection, command-brief creation, deterministic artifact output, and fixture-tested demo behavior without waking the full workforce as live execution.

## Next Recommended Step
Next recommended step: add persistent runtime index, resumable run registry, and controlled execution adapters.
