#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

JSON_FILES = [
    ROOT / '04_workflow_templates/family_007_devinized_engineering_overload_pack.json',
    ROOT / '04_workflow_templates/devinization_pack_001_command_brain.json',
    ROOT / '04_workflow_templates/devinization_pack_002_runtime_routing_work_control.json',
    ROOT / '04_workflow_templates/devinization_pack_003_prompt_memory_context_architecture.json',
    ROOT / '04_workflow_templates/devinization_pack_004_execution_safety_tools_recovery.json',
    ROOT / '04_workflow_templates/devinization_pack_005_quality_standards_human_review.json',
    ROOT / '04_workflow_templates/devinization_pack_006_output_assembly_delivery_intelligence.json',
    ROOT / '04_workflow_templates/devinization_pack_007_agent_governance_identity_accountability.json',
]

MD_FILES = [
    ROOT / '09_exports/family_007_devinized_engineering_overload_report.md',
    ROOT / '09_exports/devinization_pack_001_command_brain_report.md',
    ROOT / '09_exports/devinization_pack_002_runtime_routing_work_control_report.md',
    ROOT / '09_exports/devinization_pack_003_prompt_memory_context_architecture_report.md',
    ROOT / '09_exports/devinization_pack_004_execution_safety_tools_recovery_report.md',
    ROOT / '09_exports/devinization_pack_005_quality_standards_human_review_report.md',
    ROOT / '09_exports/devinization_pack_006_output_assembly_delivery_intelligence_report.md',
    ROOT / '09_exports/devinization_pack_007_agent_governance_identity_accountability_report.md',
    ROOT / '09_exports/final_devinization_stack_lock_report.md',
    ROOT / '09_exports/pre_hiring_devinization_note.md',
]

EXPECTED = {
    'project_owner': 'Devin O’Rourke',
    'project_owner_ascii': "Devin O'Rourke",
    'system_architect': 'Devin O’Rourke',
    'operating_doctrine_author': 'Devin O’Rourke',
    'maintainer': 'Devin O’Rourke',
    'ownership_phrase': 'Project owner, system architect, and operating-doctrine author: Devin O’Rourke.',
    'applies_to': 'Agent Command Center Devinization overlay architecture',
    'scope': 'metadata attribution only',
}
BASELINE_SNIPPETS = [
    'locked 175-family baseline remains preserved',
    'Devin O’Rourke',
    'Devinization overlay stack',
]
MD_REQUIRED = [
    '## Ownership / Attribution',
    'Project owner, system architect, and operating-doctrine author: Devin O’Rourke.',
    'Agent Command Center Devinization overlay architecture',
    'locked 175-family baseline remains preserved',
    'Devin O’Rourke',
    'owner/architect of the Devinization overlay stack',
]

errors: list[str] = []

for path in JSON_FILES:
    if not path.exists():
        errors.append(f'missing JSON file: {path.relative_to(ROOT)}')
        continue
    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        errors.append(f'failed to parse JSON {path.relative_to(ROOT)}: {exc}')
        continue
    meta = data.get('ownership_metadata')
    if not isinstance(meta, dict):
        errors.append(f'missing ownership_metadata in {path.relative_to(ROOT)}')
        continue
    for key, expected in EXPECTED.items():
        actual = meta.get(key)
        if actual != expected:
            errors.append(f'{path.relative_to(ROOT)} ownership_metadata.{key} expected {expected!r} got {actual!r}')
    baseline_note = meta.get('baseline_note', '')
    for snippet in BASELINE_SNIPPETS:
        if snippet not in baseline_note:
            errors.append(f'{path.relative_to(ROOT)} ownership_metadata.baseline_note missing snippet: {snippet}')

for path in MD_FILES:
    if not path.exists():
        errors.append(f'missing Markdown file: {path.relative_to(ROOT)}')
        continue
    text = path.read_text()
    for needle in MD_REQUIRED:
        if needle not in text:
            errors.append(f'{path.relative_to(ROOT)} missing required text: {needle}')

print('Manual scope check required: confirm git diff contains only the allowed metadata files and this validator.')
if errors:
    for error in errors:
        print(error)
    print('FAIL')
    sys.exit(1)

print('PASS: Devin ownership metadata valid.')
