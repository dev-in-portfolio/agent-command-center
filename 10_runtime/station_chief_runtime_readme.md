# Station Chief Runtime Skeleton

## Status
Station Chief Runtime upgraded to v0.4.0. Locked 175-family baseline preserved.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, optionally writes runtime artifacts, optionally updates a persistent run registry, supports resume-by-run-id lookup, supports controlled no-op adapter simulation, and supports human-confirmed sandbox file-operation gates.

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
- Writes optional runtime_index.json
- Writes optional run_registry.json
- Supports resume-by-run-id lookup
- Supports controlled no-op execution adapter simulation
- Supports controlled sandbox file-operation planning
- Supports human-confirmed sandbox file writes
- Blocks unsafe or unconfirmed file operations
- Runs deterministic fixture tests
- Supports check please, blueberry pancakes, Square Block Square Hole, Speed Racer, build, route, repair, governance, and final output command types

## What This Does Not Do
- Does not modify baseline family files
- Does not regenerate exports
- Does not connect live APIs
- Does not animate all 47,250 worker agents
- Does not execute real repo work orders yet
- Does not write to protected baseline or overlay paths
- Does not build UI yet
- Does not claim production readiness

## Commands
```bash
python3 10_runtime/station_chief_runtime.py --demo
python3 10_runtime/station_chief_runtime.py --command "check please" --json
python3 10_runtime/station_chief_runtime.py --command "build Station Chief runtime skeleton" --brief
python3 10_runtime/station_chief_runtime.py --list-overlays
python3 10_runtime/station_chief_runtime.py --list-adapters
python3 10_runtime/station_chief_runtime.py --command "check please" --simulate-adapter
python3 10_runtime/station_chief_runtime.py --command "check please" --plan-file-operation --execution-dir /tmp/station_chief_execution
python3 10_runtime/station_chief_runtime.py --command "check please" --execute-sandbox-file-write --execution-dir /tmp/station_chief_execution --confirm-execution YES_I_APPROVE_SANDBOX_FILE_WRITE
python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs --registry-dir /tmp/station_chief_registry
python3 10_runtime/station_chief_runtime.py --resume-run-id RUN_ID --registry-dir /tmp/station_chief_registry
python3 10_runtime/station_chief_runtime.py --fixture-test
python3 10_runtime/station_chief_fixture_tests.py
```

## Runtime Artifacts
When `--write-artifacts` is used, the runtime creates a deterministic run directory containing:
- run_log.json
- command_brief.json
- work_orders.json
- selected_overlays.json
- evidence.json
- execution_plan.json
- adapter_result.json
- file_operation_plan.json
- execution_gate.json
- file_operation_result.json
- runtime_index_entry.json
- manifest.json
- full_result.json

When `--registry-dir` is used with `--write-artifacts`, the runtime also writes:
- run_registry.json
- runtime_index.json

## Controlled File-Operation Gate
Runtime v0.4.0 includes a human-confirmed sandbox file-operation gate. File writes require an execution directory, a safe target path inside that directory, and the confirmation token `YES_I_APPROVE_SANDBOX_FILE_WRITE`. Protected baseline and overlay paths are blocked.

## Runtime Doctrine
The Station Chief runtime keeps the full 175-family command civilization intact while activating only the logic needed for a specific task. Runtime v0.4.0 proves command intake, classification, overlay loading, activation-tier selection, command-brief creation, deterministic artifact output, run registry tracking, resume lookup, controlled no-op adapter behavior, and human-confirmed sandbox file-operation gates without waking the full workforce as live execution.

## Next Recommended Step
Next recommended step: add human-approved repo patch adapters with changed-file scope enforcement.
