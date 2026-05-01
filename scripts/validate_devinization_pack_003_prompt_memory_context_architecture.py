import json
import os
import sys

JSON_PATH = "04_workflow_templates/devinization_pack_003_prompt_memory_context_architecture.json"
REPORT_PATH = "09_exports/devinization_pack_003_prompt_memory_context_architecture_report.md"
EXPECTED_FAMILIES = [
    {
        "family_id": 53,
        "family_name": "Prompt Systems & Instruction Architecture"
    },
    {
        "family_id": 54,
        "family_name": "Memory Engineering & Context Architecture"
    },
    {
        "family_id": 81,
        "family_name": "Agent Memory Governance & Recall Control"
    },
    {
        "family_id": 93,
        "family_name": "Conversation Design & Dialogue Systems"
    },
    {
        "family_id": 101,
        "family_name": "Cross-Project Intelligence & Pattern Transfer"
    },
    {
        "family_id": 103,
        "family_name": "Attention Management & Cognitive Workspace"
    },
    {
        "family_id": 107,
        "family_name": "Personal Archive, Vaults & Shelving Systems"
    },
    {
        "family_id": 175,
        "family_name": "Master Archive / Library of Alexandria"
    }
]
EXPECTED_MEMORY_LAYERS = [
    {
        "layer": 1,
        "name": "Immediate Conversation Context",
        "purpose": "Use current-turn and recent-turn information before asking repeated questions."
    },
    {
        "layer": 2,
        "name": "Active Project State",
        "purpose": "Track current project, current phase, active files, open tasks, blocked items, and next action."
    },
    {
        "layer": 3,
        "name": "User Preference Memory",
        "purpose": "Apply Devin’s formatting, tone, execution, shortcut, and workflow preferences."
    },
    {
        "layer": 4,
        "name": "Command Language Memory",
        "purpose": "Resolve shorthand commands, code phrases, modes, and trigger phrases."
    },
    {
        "layer": 5,
        "name": "Project Archive Memory",
        "purpose": "Store durable project decisions, corrections, lock reports, baseline states, and implementation notes."
    },
    {
        "layer": 6,
        "name": "Cross-Project Pattern Memory",
        "purpose": "Transfer lessons, structures, failure patterns, and reusable approaches across projects."
    },
    {
        "layer": 7,
        "name": "Master Archive Memory",
        "purpose": "Maintain long-term continuity, searchable archive paths, and retrieval rules across the full Agent Command Center."
    }
]
EXPECTED_CREWS = [
    [
        "DV.P3.001",
        "Station Chief Prompt Architecture Crew"
    ],
    [
        "DV.P3.002",
        "Role Prompt Template Crew"
    ],
    [
        "DV.P3.003",
        "Prompt Scope Guard Crew"
    ],
    [
        "DV.P3.004",
        "Prompt QA Crew"
    ],
    [
        "DV.P3.006",
        "Prompt Library Crew"
    ],
    [
        "DV.P3.007",
        "Context Architecture Crew"
    ],
    [
        "DV.P3.008",
        "Active Project State Crew"
    ],
    [
        "DV.P3.009",
        "Context Compression Crew"
    ],
    [
        "DV.P3.010",
        "Context Injection Crew"
    ],
    [
        "DV.P3.011",
        "Memory Injection Crew"
    ],
    [
        "DV.P3.012",
        "Memory Conflict Crew"
    ],
    [
        "DV.P3.013",
        "Recall Permission Crew"
    ],
    [
        "DV.P3.014",
        "Recall Filter Crew"
    ],
    [
        "DV.P3.015",
        "Memory Freshness Crew"
    ],
    [
        "DV.P3.016",
        "Memory Lock Crew"
    ],
    [
        "DV.P3.018",
        "Memory Audit Crew"
    ],
    [
        "DV.P3.019",
        "Thread Continuity Crew"
    ],
    [
        "DV.P3.020",
        "Dialogue Mode Crew"
    ],
    [
        "DV.P3.021",
        "Question Minimization Crew"
    ],
    [
        "DV.P3.023",
        "Dialogue Boundary Crew"
    ],
    [
        "DV.P3.024",
        "Misfire Prevention Crew"
    ],
    [
        "DV.P3.025",
        "Pattern Transfer Crew"
    ],
    [
        "DV.P3.026",
        "Cross-Project Lesson Crew"
    ],
    [
        "DV.P3.028",
        "Failure Pattern Crew"
    ],
    [
        "DV.P3.031",
        "Cognitive Workspace Index Crew"
    ],
    [
        "DV.P3.032",
        "Focus Guard Crew"
    ],
    [
        "DV.P3.036",
        "Working Memory Budget Crew"
    ],
    [
        "DV.P3.037",
        "Personal Archive Intake Crew"
    ],
    [
        "DV.P3.038",
        "Vault Structure Crew"
    ],
    [
        "DV.P3.040",
        "Retrieval Pathway Crew"
    ],
    [
        "DV.P3.041",
        "Continuity Archive Crew"
    ],
    [
        "DV.P3.043",
        "Historical Thread Linking Crew"
    ],
    [
        "DV.P3.044",
        "Master Catalog Crew"
    ],
    [
        "DV.P3.045",
        "Source Preservation Crew"
    ],
    [
        "DV.P3.046",
        "Archive Retrieval QA Crew"
    ],
    [
        "DV.P3.047",
        "Archive Continuity Lock Crew"
    ],
    [
        "DV.P3.048",
        "Alexandria Librarian Crew"
    ]
]
EXPECTED_ROLES = [
    "Realist",
    "Overachiever",
    "Dreamer",
    "Timid",
    "Overprotective",
    "Wildcard Intern",
    "Team Lead / Manager",
    "Scribe / Shower of Work",
    "Auditor / Revision Director"
]
REQUIRED_JSON_PHRASES = [
    "Station Chief",
    "prompt architecture",
    "memory layers",
    "active project state",
    "context compression",
    "memory injection",
    "recall filter",
    "blueberry pancakes",
    "check please",
    "thread continuity",
    "cross-project pattern",
    "cognitive workspace",
    "archive",
    "vault",
    "Master Archive",
    "Library of Alexandria",
    "source of truth",
    "context soup"
]
REQUIRED_REPORT_PHRASES = [
    "Overlay created. Locked 175-family baseline preserved.",
    "Station Chief prompt architecture",
    "memory layer separation",
    "active project state",
    "context compression",
    "recall filtering",
    "master archive retrieval",
    "The Agent Command Center does not treat memory as one bucket.",
    "Next recommended build step"
]


def add_error(errors, message):
    errors.append(message)


def main():
    errors = []
    print("Manual scope check required: confirm git diff contains only the three allowed files.")

    if not os.path.exists(JSON_PATH):
        add_error(errors, f"File missing: {JSON_PATH}")
    if not os.path.exists(REPORT_PATH):
        add_error(errors, f"File missing: {REPORT_PATH}")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    if data.get("extension_id") != "devinization_pack_003_prompt_memory_context_architecture":
        add_error(errors, "JSON: extension_id mismatch")
    if data.get("extension_name") != "Devinization Pack 3 — Prompt, Memory & Context Architecture":
        add_error(errors, "JSON: extension_name mismatch")
    if data.get("mode") != "overlay":
        add_error(errors, "JSON: mode mismatch")
    if data.get("preserves_locked_baseline") is not True:
        add_error(errors, "JSON: preserves_locked_baseline must be true")
    if data.get("baseline_status") != "175-family expansion locked":
        add_error(errors, "JSON: baseline_status mismatch")

    if data.get("included_families") != EXPECTED_FAMILIES:
        add_error(errors, "JSON: included_families mismatch")
    if len(data.get("included_families", [])) != 8:
        add_error(errors, f"JSON: expected 8 included families, found {len(data.get('included_families', []))}")

    if data.get("memory_layers") != EXPECTED_MEMORY_LAYERS:
        add_error(errors, "JSON: memory_layers mismatch")
    if len(data.get("memory_layers", [])) != 7:
        add_error(errors, f"JSON: expected 7 memory layers, found {len(data.get('memory_layers', []))}")

    depends_on = data.get("depends_on", [])
    for required in ["family_007_devinized_engineering_overload", "devinization_pack_001_command_brain", "devinization_pack_002_runtime_routing_work_control"]:
        if required not in depends_on:
            add_error(errors, f"JSON: depends_on missing {required}")

    crews = data.get("crews", [])
    if len(crews) != 48:
        add_error(errors, f"JSON: expected 48 crews, found {len(crews)}")

    found_crews = {crew.get("crew_id"): crew.get("crew_name") for crew in crews}
    expected_ids = {crew_id for crew_id, _ in EXPECTED_CREWS}
    for crew_id, crew_name in EXPECTED_CREWS:
        actual_name = found_crews.get(crew_id)
        if actual_name is None:
            add_error(errors, f"JSON: required crew ID {crew_id} missing")
        elif actual_name != crew_name:
            add_error(errors, f"JSON: crew name mismatch for {crew_id}. Expected '{crew_name}', found '{actual_name}'")
    required_fields = ["crew_id", "crew_name", "family_anchor", "mission", "triggers", "primary_outputs", "handoff_targets", "roles"]
    for crew in crews:
        crew_id = crew.get("crew_id", "<missing crew_id>")
        missing = [field for field in required_fields if field not in crew]
        if missing:
            add_error(errors, f"Crew {crew_id}: missing fields {', '.join(missing)}")
            continue
        roles = crew.get("roles", [])
        if len(roles) != 9:
            add_error(errors, f"Crew {crew_id}: expected 9 roles, found {len(roles)}")
            continue
        for index, expected_role in enumerate(EXPECTED_ROLES):
            role_obj = roles[index]
            expected_role_id = f"{crew_id}.1{chr(ord('A') + index)}"
            if not isinstance(role_obj, dict):
                add_error(errors, f"Crew {crew_id}: role {index} is not an object")
                continue
            if role_obj.get("id") != expected_role_id:
                add_error(errors, f"Crew {crew_id}: role {index} id mismatch")
            if role_obj.get("role") != expected_role:
                add_error(errors, f"Crew {crew_id}: role {index} name mismatch")

    json_text_lower = json.dumps(data, ensure_ascii=False).lower()
    for phrase in REQUIRED_JSON_PHRASES:
        if phrase.lower() not in json_text_lower:
            add_error(errors, f"JSON: required phrase '{phrase}' missing")

    with open(REPORT_PATH, "r", encoding="utf-8") as handle:
        report = handle.read().lower()
    for phrase in REQUIRED_REPORT_PHRASES:
        if phrase.lower() not in report:
            add_error(errors, f"Report: required phrase '{phrase}' missing")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print("PASS: Devinization Pack 3 Prompt, Memory & Context Architecture valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()
