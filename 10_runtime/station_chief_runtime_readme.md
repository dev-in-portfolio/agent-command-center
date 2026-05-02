# Station Chief Runtime Skeleton

## Status
Station Chief Runtime upgraded to v2.1.0. Locked 175-family baseline preserved. Single-worker tool permission binding added.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, writes deterministic artifacts, supports registry/resume, supports gated sandbox and scoped repo patch operations, supports dry-run/approval/ledger/release-lock flows, supports controlled execution profile expansion, supports a dry-run-only work order executor skeleton, supports worker hiring registry preview, supports department routing runtime preview, supports a multi-agent orchestration sandbox, supports UI/operator console schemas, supports GitHub patch application hardening, supports a deployment/portfolio packaging bridge, supports first controlled single-worker sandbox execution, and now adds single-worker tool permission binding.

## What This Adds
- single-worker tool permission binding schema
- per-tool permission registry
- tool-specific approval tokens
- tool permission request validator
- tool-specific approval binding
- tool invocation dry-run contract
- tool output validation schema
- tool output validation result
- tool failure handling contract
- tool revocation contract
- per-run permission audit proof
- tool permission ledger
- tool permission readiness summary
- live execution telemetry and abort controls readiness bridge
- tool permission binding artifact writing
- tool permission binding manifest

## What This Does Not Do
- Does not modify baseline family files
- Does not regenerate exports
- Does not connect live APIs
- Does not call hosting APIs
- Does not deploy to Netlify, Vercel, Cloudflare, Firebase, Railway, Render, GitHub Pages, or external platforms
- Does not animate all 47,250 worker agents
- Does not hire real worker agents
- Does not execute uncontrolled repo work orders
- Does not execute arbitrary code
- Does not run shell commands
- Does not execute live external tools
- Does not invoke external tools
- Does not assign broad live workers
- Does not route live workers
- Does not perform live orchestration
- Does not render a live UI
- Does not start a server
- Does not call GitHub APIs
- Does not apply uncontrolled repo patches
- Does not push commits
- Does not write to protected baseline or overlay paths
- Does not treat tool permission binding as broad execution permission
- Does not build live execution telemetry and abort controls yet
- Does not claim full Agent Command Center production completion
- no live UI rendering
- no live orchestration
- no live worker routing
- no real worker hiring
- no worker animation
- no uncontrolled repo edits
- no GitHub API mutation
- no patch execution authorization
- no live deployment
- no hosting API calls
- no external service mutation
- no broad workforce animation
- no external execution
- no arbitrary code execution
- no shell commands

## Commands

python3 10_runtime/station_chief_runtime.py --demo

python3 10_runtime/station_chief_runtime.py --tool-permission-schema

python3 10_runtime/station_chief_runtime.py --command "check please" --tool-permission-binding

python3 10_runtime/station_chief_runtime.py --command "check please" --tool-permission-binding --tool-permission-request deterministic_summary --tool-permission-token deterministic_summary=YES_I_APPROVE_TOOL_DETERMINISTIC_SUMMARY

python3 10_runtime/station_chief_runtime.py --command "build live execution telemetry and abort controls" --tool-permission-binding --tool-permission-request deterministic_summary --tool-permission-token deterministic_summary=YES_I_APPROVE_TOOL_DETERMINISTIC_SUMMARY

python3 10_runtime/station_chief_runtime.py --command "check please" --write-tool-permission-binding /tmp/station_chief_tool_permission_binding --tool-permission-request sandbox_noop --tool-permission-token sandbox_noop=YES_I_APPROVE_TOOL_SANDBOX_NOOP

python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs --registry-dir /tmp/station_chief_registry --tool-permission-binding --tool-permission-request deterministic_summary --tool-permission-token deterministic_summary=YES_I_APPROVE_TOOL_DETERMINISTIC_SUMMARY

python3 10_runtime/station_chief_runtime.py --fixture-test

python3 10_runtime/station_chief_fixture_tests.py

## Tool Permission Binding Artifacts

When --write-tool-permission-binding is used, the runtime creates:
- tool_permission_binding_bundle.json
- tool_permission_binding_schema.json
- per_tool_permission_registry.json
- tool_permission_request_validation.json
- tool_specific_approval_binding.json
- tool_invocation_dry_run_contract.json
- tool_output_validation_schema.json
- tool_output_validation_result.json
- tool_failure_handling_contract.json
- tool_revocation_contract.json
- per_run_permission_audit_proof.json
- tool_permission_ledger.json
- tool_permission_readiness_summary.json
- live_execution_telemetry_abort_readiness_bridge.json
- tool_permission_binding_manifest.json

## Runtime Doctrine

Station Chief Runtime v2.1.0 adds Single-Worker Tool Permission Binding without granting unbounded tool access or external execution. It creates per-tool permission registries, tool-specific approval-token bindings, permission request validators, dry-run invocation contracts, output validation schemas and results, failure handling contracts, revocation contracts, per-run permission audit proofs, tool permission ledgers, readiness summaries, and live execution telemetry/abort handoff records while preserving the locked 175-family baseline, avoiding live external actions, avoiding external tool invocation, avoiding shell commands, avoiding arbitrary code execution, avoiding hosting API calls, avoiding live deployment, avoiding uncontrolled repo edits, avoiding baseline mutation, avoiding Devinization overlay mutation, and avoiding repo file modification.

## Next Recommended Step
Next recommended step: build live execution telemetry and abort controls.
