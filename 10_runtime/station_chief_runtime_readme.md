# Station Chief Runtime Skeleton

## Status
Station Chief Runtime upgraded to v1.6.0. Locked 175-family baseline preserved. UI/operator console schema added.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, writes deterministic artifacts, supports registry/resume, supports gated sandbox and scoped repo patch operations, supports dry-run/approval/ledger/release-lock flows, supports controlled execution profile expansion, supports a dry-run-only work order executor skeleton, supports worker hiring registry preview, supports department routing runtime preview, supports a multi-agent orchestration sandbox, and now adds a UI/operator console schema layer.

## What This Adds
- operator console screen schema
- runtime status panel schema
- approval queue panel schema
- work order panel schema
- worker registry panel schema
- department routing panel schema
- orchestration sandbox panel schema
- release lock panel schema
- human control surface schema
- operator action registry
- disabled action state map
- read_only operator console review bundle
- operator console safety summary
- operator console readiness summary
- GitHub patch hardening readiness bridge
- operator console artifact writing
- operator console manifest

## What This Does Not Do
- Does not modify baseline family files
- Does not regenerate exports
- Does not connect live APIs
- Does not animate all 47,250 worker agents
- Does not hire real worker agents
- Does not execute uncontrolled repo work orders
- Does not execute live work orders
- Does not assign live workers
- Does not route live workers
- Does not perform live orchestration
- Does not render a live UI
- Does not start a server
- no live UI rendering
- no live orchestration
- no live worker routing
- no real worker hiring
- no worker animation
- Does not write to protected baseline or overlay paths
- Does not treat operator console schemas as execution permission
- Does not build GitHub patch hardening yet
- Does not claim full Agent Command Center production completion

## Commands

python3 10_runtime/station_chief_runtime.py --demo

python3 10_runtime/station_chief_runtime.py --operator-console-schema

python3 10_runtime/station_chief_runtime.py --command "check please" --operator-console

python3 10_runtime/station_chief_runtime.py --command "build GitHub patch application hardening" --operator-console

python3 10_runtime/station_chief_runtime.py --command "check please" --write-operator-console /tmp/station_chief_operator_console

python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs --registry-dir /tmp/station_chief_registry --operator-console

python3 10_runtime/station_chief_runtime.py --fixture-test

python3 10_runtime/station_chief_fixture_tests.py

## Operator Console Artifacts

When --write-operator-console is used, the runtime creates:
- operator_console_bundle.json
- operator_console_review_bundle.json
- operator_console_screen_schema.json
- runtime_status_panel_schema.json
- approval_queue_panel_schema.json
- work_order_panel_schema.json
- worker_registry_panel_schema.json
- department_routing_panel_schema.json
- orchestration_sandbox_panel_schema.json
- release_lock_panel_schema.json
- human_control_surface_schema.json
- operator_action_registry.json
- disabled_action_state_map.json
- operator_console_safety_summary.json
- operator_console_readiness_summary.json
- github_patch_hardening_readiness_bridge.json
- operator_console_manifest.json

## Runtime Doctrine

Station Chief Runtime v1.6.0 adds the UI / Operator Console Schema without rendering a live UI or authorizing execution. It creates operator console screen schemas, runtime status panels, approval queue panels, work order panels, worker registry panels, department routing panels, orchestration sandbox panels, release lock panels, human control surfaces, operator action registries, disabled action maps, read-only review bundles, safety summaries, readiness summaries, and GitHub patch hardening handoff records while preserving the locked 175-family baseline, avoiding live external actions, avoiding worker animation, avoiding real worker hiring, avoiding live worker routing, avoiding live orchestration, avoiding live UI rendering, and avoiding repo file modification.

## Next Recommended Step
Next recommended step: build GitHub patch application hardening.
