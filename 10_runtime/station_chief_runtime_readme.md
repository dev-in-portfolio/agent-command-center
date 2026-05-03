# Station Chief Runtime Skeleton

## Status
Station Chief Runtime upgraded to v2.5.0. Locked 175-family baseline preserved. Controlled external tool adapter preview added.

## Purpose
The Station Chief runtime receives one command, classifies it, loads the locked Devinization overlay stack, selects an activation tier, creates a command brief, creates non-executing work orders, writes deterministic artifacts, supports registry/resume, supports gated sandbox and scoped repo patch operations, supports dry-run/approval/ledger/release-lock flows, supports controlled execution profile expansion, supports a dry-run-only work order executor skeleton, supports worker hiring registry preview, supports department routing runtime preview, supports a multi-agent orchestration sandbox, supports UI/operator console schemas, supports GitHub patch application hardening, supports a deployment/portfolio packaging bridge, supports first controlled single-worker sandbox execution, supports single-worker tool permission binding, supports live execution telemetry and abort controls, supports post-run audit proof expansion, supports multi-worker sandbox coordination, and now adds controlled external tool adapter preview.

## What This Adds
- controlled external tool adapter preview schema
- external tool adapter preview approval gate
- external tool dry-run adapter registry
- per-tool external permission gate
- external request preview contract
- external response validation schema
- external response validation preview result
- external tool abort contract
- external tool audit proof
- external tool preview ledger
- external tool preview readiness summary
- permissioned external API dry-run preview readiness bridge
- controlled external tool adapter preview artifact writing
- controlled external tool adapter preview manifest

## Exact Compatibility Terms
- multi-worker sandbox coordination schema
- controlled external tool adapter preview readiness bridge
- no broad workforce animation
- no external API calls
- no external artifact fetching
- no actual replay execution
- no process termination
- no shell command execution
- no arbitrary code execution
- no repo mutation
- no deployment
- Station Chief Runtime v2.5.0 adds Multi-Worker Sandbox Coordination without full workforce animation, real worker hiring, worker process creation, live routing, live orchestration, external API calls, or broad execution
- Station Chief Runtime v2.5.0 adds Controlled External Tool Adapter Preview without external tool invocation, live API calls, network access, socket access, deployment, or broad execution

## What This Does Not Do
- Does not modify baseline family files
- Does not regenerate exports
- Does not connect live APIs
- Does not invoke external tools
- Does not make network requests
- Does not open sockets
- Does not fetch external artifacts
- Does not send external telemetry
- Does not call hosting APIs
- Does not deploy to Netlify, Vercel, Cloudflare, Firebase, Railway, Render, GitHub Pages, or external platforms
- Does not animate all 47,250 worker agents
- Does not hire real worker agents
- Does not start worker processes
- Does not execute uncontrolled repo work orders
- Does not execute arbitrary code
- Does not run shell commands
- Does not terminate processes
- Does not start background monitoring
- Does not perform actual replay execution
- Does not assign broad live workers
- Does not route live workers
- Does not perform live orchestration
- Does not render a live UI
- Does not start a server
- Does not call GitHub APIs
- Does not apply uncontrolled repo patches
- Does not push commits
- Does not write to protected baseline or overlay paths
- Does not treat controlled external tool adapter preview as external execution permission
- Does not build permissioned external API dry-run preview yet
- Does not claim full Agent Command Center production completion

## Commands

python3 10_runtime/station_chief_runtime.py --demo

python3 10_runtime/station_chief_runtime.py --external-tool-preview-schema

python3 10_runtime/station_chief_runtime.py --command "check please" --controlled-external-tool-preview

python3 10_runtime/station_chief_runtime.py --command "check please" --controlled-external-tool-preview --external-tool-confirm-token YES_I_APPROVE_CONTROLLED_EXTERNAL_TOOL_ADAPTER_PREVIEW

python3 10_runtime/station_chief_runtime.py --command "build permissioned external API dry-run preview" --controlled-external-tool-preview --external-tool-confirm-token YES_I_APPROVE_CONTROLLED_EXTERNAL_TOOL_ADAPTER_PREVIEW

python3 10_runtime/station_chief_runtime.py --command "check please" --controlled-external-tool-preview --external-tool-confirm-token YES_I_APPROVE_CONTROLLED_EXTERNAL_TOOL_ADAPTER_PREVIEW --external-tool-id github_read_preview --external-tool-requested-tool github_read_preview

python3 10_runtime/station_chief_runtime.py --command "check please" --controlled-external-tool-preview --external-tool-confirm-token YES_I_APPROVE_CONTROLLED_EXTERNAL_TOOL_ADAPTER_PREVIEW --external-tool-response-preview-json '{"tool_id":"web_search_preview","response_status":"PASS","response_payload":{"bad":"api_key=123"},"response_digest":"bad","external_actions_taken":false,"live_api_call_performed":false,"repo_files_modified":false,"execution_authorized":false}'

python3 10_runtime/station_chief_runtime.py --command "check please" --write-controlled-external-tool-preview /tmp/station_chief_external_tool_preview --external-tool-confirm-token YES_I_APPROVE_CONTROLLED_EXTERNAL_TOOL_ADAPTER_PREVIEW

python3 10_runtime/station_chief_runtime.py --command "check please" --write-artifacts /tmp/station_chief_runs --registry-dir /tmp/station_chief_registry --controlled-external-tool-preview --external-tool-confirm-token YES_I_APPROVE_CONTROLLED_EXTERNAL_TOOL_ADAPTER_PREVIEW

python3 10_runtime/station_chief_runtime.py --fixture-test

python3 10_runtime/station_chief_fixture_tests.py

## Controlled External Tool Adapter Preview Artifacts

When --write-controlled-external-tool-preview is used, the runtime creates:
- controlled_external_tool_adapter_preview_bundle.json
- controlled_external_tool_adapter_preview_schema.json
- external_tool_adapter_preview_approval_gate.json
- external_tool_dry_run_adapter_registry.json
- per_tool_external_permission_gate.json
- external_request_preview_contract.json
- external_response_validation_schema.json
- external_response_validation_preview_result.json
- external_tool_abort_contract.json
- external_tool_audit_proof.json
- external_tool_preview_ledger.json
- external_tool_preview_readiness_summary.json
- permissioned_external_api_dry_run_preview_readiness_bridge.json
- controlled_external_tool_adapter_preview_manifest.json

## Runtime Doctrine

Station Chief Runtime v2.5.0 adds Controlled External Tool Adapter Preview without external tool invocation, live API calls, network access, socket access, deployment, or broad execution. It creates deterministic external tool adapter preview schemas, approval gates, dry-run adapter registries, per-tool external permission gates, request preview contracts, response validation schemas and preview results, external tool abort contracts, external tool audit proofs, preview ledgers, readiness summaries, and permissioned external API dry-run preview handoff records while preserving the locked 175-family baseline, avoiding live external actions, avoiding external tool invocation, avoiding live API calls, avoiding network access, avoiding socket access, avoiding shell commands, avoiding arbitrary code execution, avoiding hosting API calls, avoiding live deployment, avoiding uncontrolled repo edits, avoiding baseline mutation, avoiding Devinization overlay mutation, and avoiding repo file modification.

## Next Recommended Step
Next recommended step: build permissioned external API dry-run preview.
