#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / '10_runtime/station_chief_runtime.py',
    ROOT / '10_runtime/station_chief_demo_cases.json',
    ROOT / '10_runtime/station_chief_runtime_readme.md',
    ROOT / '09_exports/station_chief_runtime_skeleton_report.md',
    ROOT / 'scripts/validate_station_chief_runtime_skeleton.py',
]

errors: list[str] = []
for path in FILES:
    if not path.exists():
        errors.append(f'missing file: {path.relative_to(ROOT)}')

runtime_text = (ROOT / '10_runtime/station_chief_runtime.py').read_text() if (ROOT / '10_runtime/station_chief_runtime.py').exists() else ''
required_snippets = [
    'STATION_CHIEF_RUNTIME_VERSION = "0.2.0"',
    'EXPECTED_OVERLAYS',
    'load_overlay_stack',
    'classify_command',
    'determine_activation_tier',
    'select_overlays',
    'create_command_brief',
    'create_work_orders',
    'run_station_chief',
    'run_fixture_tests',
    'deterministic_demo_mode',
    'baseline_protection',
    'workforce_animation_allowed',
    'external_actions_allowed',
]
for snippet in required_snippets:
    if snippet not in runtime_text:
        errors.append(f'runtime missing snippet: {snippet}')
for forbidden in ['requests', 'urllib.request', 'subprocess', 'os.system', 'pip install', 'npm install']:
    if forbidden in runtime_text:
        errors.append(f'runtime contains forbidden snippet: {forbidden}')

cases_path = ROOT / '10_runtime/station_chief_demo_cases.json'
if cases_path.exists():
    try:
        cases = json.loads(cases_path.read_text())
        demo_cases = cases.get('demo_cases')
        if not isinstance(demo_cases, list) or len(demo_cases) != 5:
            errors.append('demo cases JSON must contain exactly 5 demo cases')
        else:
            expected_ids = {'demo_check_please', 'demo_build_runtime', 'demo_blueberry_pancakes', 'demo_square_block', 'demo_agent_court'}
            ids = {case.get('case_id') for case in demo_cases}
            missing = expected_ids - ids
            if missing:
                errors.append(f'demo cases missing ids: {sorted(missing)}')
    except Exception as exc:
        errors.append(f'failed to parse demo cases JSON: {exc}')

README = ROOT / '10_runtime/station_chief_runtime_readme.md'
REPORT = ROOT / '09_exports/station_chief_runtime_skeleton_report.md'
for path, required in [
    (README, [
        'Station Chief Runtime Skeleton',
        'Initial runnable runtime skeleton upgraded to v0.2.0.',
        'one-command intake',
        'command classification',
        'activation-tier selection',
        'deterministic demo output',
        'optional runtime artifacts',
        'deterministic fixture tests',
        'Does not animate all 47,250 worker agents',
        'The Station Chief runtime skeleton keeps the full 175-family command civilization intact',
    ]),
    (REPORT, [
        'Station Chief Runtime Skeleton Report',
        'Initial runnable runtime skeleton upgraded to v0.2.0. Locked 175-family baseline preserved.',
        'Project owner, system architect, and operating-doctrine author: Devin O’Rourke.',
        'one-command intake',
        'command classification',
        'activation tier selection',
        'overlay stack loading',
        'command brief generation',
        'non-executing work order generation',
        'persistent run log artifacts',
        'command brief artifact output',
        'work order artifact output',
        'selected overlay artifact output',
        'evidence artifact output',
        'deterministic fixture tests',
        'deterministic demo mode',
        'no live API calls',
        'no full workforce animation',
        'Next recommended build step',
    ]),
]:
    if path.exists():
        text = path.read_text()
        for item in required:
            if item not in text:
                errors.append(f'{path.relative_to(ROOT)} missing required text: {item}')

print('Manual scope check required: confirm git diff contains only the five allowed Station Chief runtime skeleton files.')

# Runtime command checks via subprocess are allowed here only.

def run_cmd(args: list[str]) -> str:
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"command failed: {' '.join(args)}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )
    return proc.stdout

try:
    demo = json.loads(run_cmd(['python3', '10_runtime/station_chief_runtime.py', '--demo']))
    if demo.get('station_chief_runtime_version') != '0.2.0':
        errors.append('demo runtime version mismatch')
    if demo.get('command_type') != 'verification':
        errors.append('demo command_type mismatch')
    if demo.get('activation_tier', {}).get('name') != 'Tier 4 — Audit / Archive':
        errors.append('demo activation tier mismatch')
    evidence = demo.get('evidence', {})
    for key, expected in [
        ('baseline_preserved', True),
        ('external_actions_taken', False),
        ('live_worker_agents_activated', False),
        ('deterministic_demo_mode', True),
        ('validators_required_before_completion', True),
    ]:
        if evidence.get(key) is not expected:
            errors.append(f'demo evidence mismatch for {key}')
except Exception as exc:
    errors.append(str(exc))

try:
    overlays = json.loads(run_cmd(['python3', '10_runtime/station_chief_runtime.py', '--list-overlays']))
    if len(overlays) != 8:
        errors.append(f'overlay count expected 8 got {len(overlays)}')
    for overlay in overlays:
        if overlay.get('exists') is not True:
            errors.append(f'overlay not existing: {overlay.get("id")}')
        if overlay.get('preserves_locked_baseline') is not True:
            errors.append(f'overlay does not preserve baseline: {overlay.get("id")}')
        if 'Devin O’Rourke' not in str(overlay.get('ownership_project_owner')):
            errors.append(f'overlay ownership missing Devin O’Rourke: {overlay.get("id")}')
except Exception as exc:
    errors.append(str(exc))

try:
    brief = json.loads(run_cmd(['python3', '10_runtime/station_chief_runtime.py', '--command', 'build Station Chief runtime skeleton', '--brief']))
    if brief.get('command_type') != 'build':
        errors.append('brief command_type mismatch')
    if brief.get('activation_tier', {}).get('name') != 'Tier 3 — Active Operation':
        errors.append('brief activation tier mismatch')
    if brief.get('deterministic_demo_mode') is not True:
        errors.append('brief deterministic_demo_mode mismatch')
    if brief.get('baseline_protection') is not True:
        errors.append('brief baseline_protection mismatch')
    if brief.get('external_actions_allowed') is not False:
        errors.append('brief external_actions_allowed mismatch')
    if brief.get('workforce_animation_allowed') is not False:
        errors.append('brief workforce_animation_allowed mismatch')
except Exception as exc:
    errors.append(str(exc))

if errors:
    for error in errors:
        print(error)
    print('FAIL')
    sys.exit(1)

print('PASS: Station Chief Runtime Skeleton valid.')
