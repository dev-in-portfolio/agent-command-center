import json
import os
import sys

LOCK_REPORT = "09_exports/final_devinization_stack_lock_report.md"
EXPECTED_JSONS = [
    ("04_workflow_templates/family_007_devinized_engineering_overload_pack.json", "family_007_devinized_engineering_overload"),
    ("04_workflow_templates/devinization_pack_001_command_brain.json", "devinization_pack_001_command_brain"),
    ("04_workflow_templates/devinization_pack_002_runtime_routing_work_control.json", "devinization_pack_002_runtime_routing_work_control"),
    ("04_workflow_templates/devinization_pack_003_prompt_memory_context_architecture.json", "devinization_pack_003_prompt_memory_context_architecture"),
    ("04_workflow_templates/devinization_pack_004_execution_safety_tools_recovery.json", "devinization_pack_004_execution_safety_tools_recovery"),
    ("04_workflow_templates/devinization_pack_005_quality_standards_human_review.json", "devinization_pack_005_quality_standards_human_review"),
    ("04_workflow_templates/devinization_pack_006_output_assembly_delivery_intelligence.json", "devinization_pack_006_output_assembly_delivery_intelligence"),
    ("04_workflow_templates/devinization_pack_007_agent_governance_identity_accountability.json", "devinization_pack_007_agent_governance_identity_accountability"),
]
EXPECTED_REPORTS = [
    "09_exports/family_007_devinized_engineering_overload_report.md",
    "09_exports/devinization_pack_001_command_brain_report.md",
    "09_exports/devinization_pack_002_runtime_routing_work_control_report.md",
    "09_exports/devinization_pack_003_prompt_memory_context_architecture_report.md",
    "09_exports/devinization_pack_004_execution_safety_tools_recovery_report.md",
    "09_exports/devinization_pack_005_quality_standards_human_review_report.md",
    "09_exports/devinization_pack_006_output_assembly_delivery_intelligence_report.md",
    "09_exports/devinization_pack_007_agent_governance_identity_accountability_report.md",
]
EXPECTED_VALIDATORS = [
    "scripts/validate_family_007_devinized_engineering_overload_pack.py",
    "scripts/validate_devinization_pack_001_command_brain.py",
    "scripts/validate_devinization_pack_002_runtime_routing_work_control.py",
    "scripts/validate_devinization_pack_003_prompt_memory_context_architecture.py",
    "scripts/validate_devinization_pack_004_execution_safety_tools_recovery.py",
    "scripts/validate_devinization_pack_005_quality_standards_human_review.py",
    "scripts/validate_devinization_pack_006_output_assembly_delivery_intelligence.py",
    "scripts/validate_devinization_pack_007_agent_governance_identity_accountability.py",
    "scripts/validate_full_expansion_completion.py",
]
EXPECTED_COUNTS = {
    "family_007_devinized_engineering_overload": 30,
    "devinization_pack_001_command_brain": 36,
    "devinization_pack_002_runtime_routing_work_control": 42,
    "devinization_pack_003_prompt_memory_context_architecture": 48,
    "devinization_pack_004_execution_safety_tools_recovery": 42,
    "devinization_pack_005_quality_standards_human_review": 48,
    "devinization_pack_006_output_assembly_delivery_intelligence": 24,
    "devinization_pack_007_agent_governance_identity_accountability": 24,
}
REPORT_PHRASES = [
    "Family 7 and Devinization Packs 1 through 7 are locked as overlay architecture.",
    "Locked 175-family baseline preserved.",
    "The 175-family baseline remains the official org chart.",
    "Station Chief command interpretation",
    "runtime routing and work control",
    "prompt, memory, and context architecture",
    "execution safety and tool recovery",
    "quality standards and human review",
    "output assembly and delivery intelligence",
    "agent governance, identity, and accountability",
    "deterministic demo mode readiness",
    "future workforce hiring/animation",
    "Station Chief runtime skeleton",
    "The Agent Command Center is now ready to move from Devinized overlay architecture into runtime skeleton work.",
    "Next recommended build step",
]


def add_error(errors, message):
    errors.append(message)


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def count_crews(data):
    return len(data.get('crews', []))


def main():
    errors = []
    print("Manual scope check required: confirm git diff contains only the two allowed files.")

    if not os.path.exists(LOCK_REPORT):
        add_error(errors, f"File missing: {LOCK_REPORT}")

    for path, expected_id in EXPECTED_JSONS:
        if not os.path.exists(path):
            add_error(errors, f"File missing: {path}")
    for path in EXPECTED_REPORTS:
        if not os.path.exists(path):
            add_error(errors, f"File missing: {path}")
    for path in EXPECTED_VALIDATORS:
        if not os.path.exists(path):
            add_error(errors, f"File missing: {path}")

    if errors:
        print('FAIL')
        for err in errors:
            print(f'- {err}')
        sys.exit(1)

    for path, expected_id in EXPECTED_JSONS:
        data = load_json(path)
        if data.get('extension_id') != expected_id:
            add_error(errors, f"JSON: extension_id mismatch in {path}")
        if data.get('mode') != 'overlay':
            add_error(errors, f"JSON: mode mismatch in {path}")
        if data.get('preserves_locked_baseline') is not True:
            add_error(errors, f"JSON: preserves_locked_baseline must be true in {path}")

    counts = {
        'family_007_devinized_engineering_overload': 30,
        'devinization_pack_001_command_brain': 36,
        'devinization_pack_002_runtime_routing_work_control': 42,
        'devinization_pack_003_prompt_memory_context_architecture': 48,
        'devinization_pack_004_execution_safety_tools_recovery': 42,
        'devinization_pack_005_quality_standards_human_review': 48,
        'devinization_pack_006_output_assembly_delivery_intelligence': 24,
        'devinization_pack_007_agent_governance_identity_accountability': 24,
    }
    for path, expected_id in EXPECTED_JSONS:
        data = load_json(path)
        actual = len(data.get('crews', []))
        expected = counts[expected_id]
        if actual != expected:
            add_error(errors, f"JSON: expected {expected} crews in {path}, found {actual}")

    report = open(LOCK_REPORT, 'r', encoding='utf-8').read()
    for phrase in REPORT_PHRASES:
        if phrase not in report:
            add_error(errors, f"Report: required phrase '{phrase}' missing")

    if errors:
        print('FAIL')
        for err in errors:
            print(f'- {err}')
        sys.exit(1)

    print('PASS: Final Devinization Stack Lock valid.')
    sys.exit(0)


if __name__ == '__main__':
    main()
