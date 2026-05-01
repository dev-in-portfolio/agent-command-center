import json
import os
import sys

JSON_PATH = "04_workflow_templates/devinization_pack_006_output_assembly_delivery_intelligence.json"
REPORT_PATH = "09_exports/devinization_pack_006_output_assembly_delivery_intelligence_report.md"
EXPECTED_FAMILIES = [
    {
        "family_id": 138,
        "family_name": "Output Assembly, Synthesis & Final Answer Design"
    },
    {
        "family_id": 82,
        "family_name": "Version Control, Releases & Change Management"
    }
]
EXPECTED_DELIVERY_LAYERS = [
    {
        "layer": 1,
        "name": "Priority Front-Load Layer",
        "purpose": "Put the most actionable answer, status, verdict, or next step near the top instead of burying it."
    },
    {
        "layer": 2,
        "name": "Synthesis Layer",
        "purpose": "Combine work outputs, evidence, validator results, review notes, and context into one coherent final response."
    },
    {
        "layer": 3,
        "name": "Formatting & Copy/Paste Layer",
        "purpose": "Shape outputs into usable copy/paste blocks, reports, prompts, tables, or deliverable-ready structures."
    },
    {
        "layer": 4,
        "name": "Proof & Traceability Layer",
        "purpose": "Attach changed files, validator results, commit hashes, evidence, assumptions, and uncertainty notes where needed."
    },
    {
        "layer": 5,
        "name": "Audience Adaptation Layer",
        "purpose": "Adjust output for Devin, client, recruiter, portfolio, technical, operational, or public-facing use."
    },
    {
        "layer": 6,
        "name": "Version & Release Layer",
        "purpose": "Track versions, release notes, changelogs, labels, package names, and stable baselines."
    },
    {
        "layer": 7,
        "name": "Final Delivery Gate",
        "purpose": "Confirm that the output is complete, readable, scoped, validated, and ready for its intended use."
    }
]
EXPECTED_CREWS = [
    [
        "DV.P6.001",
        "Final Answer Assembly Crew"
    ],
    [
        "DV.P6.002",
        "Priority Front-Load Crew"
    ],
    [
        "DV.P6.003",
        "Synthesis Crew"
    ],
    [
        "DV.P6.004",
        "Proof Integration Crew"
    ],
    [
        "DV.P6.005",
        "Copy/Paste Output Crew"
    ],
    [
        "DV.P6.006",
        "Check Result Formatting Crew"
    ],
    [
        "DV.P6.007",
        "Partial Output Explanation Crew"
    ],
    [
        "DV.P6.008",
        "Prompt Delivery Crew"
    ],
    [
        "DV.P6.009",
        "Formatting Standard Crew"
    ],
    [
        "DV.P6.010",
        "Audience Adaptation Crew"
    ],
    [
        "DV.P6.011",
        "Next Step Design Crew"
    ],
    [
        "DV.P6.012",
        "Final Delivery Gate Crew"
    ],
    [
        "DV.P6.013",
        "Version Label Crew"
    ],
    [
        "DV.P6.014",
        "Changelog Crew"
    ],
    [
        "DV.P6.015",
        "Release Scope Crew"
    ],
    [
        "DV.P6.016",
        "Release Readiness Crew"
    ],
    [
        "DV.P6.017",
        "Change Request Routing Crew"
    ],
    [
        "DV.P6.018",
        "Release Notes Crew"
    ],
    [
        "DV.P6.019",
        "Release Evidence Crew"
    ],
    [
        "DV.P6.020",
        "Release Blocker Crew"
    ],
    [
        "DV.P6.021",
        "Change Impact Crew"
    ],
    [
        "DV.P6.022",
        "Stable Baseline Label Crew"
    ],
    [
        "DV.P6.023",
        "Portfolio / Showcase Delivery Crew"
    ],
    [
        "DV.P6.024",
        "Final Package Lock Crew"
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
    "final answer",
    "output assembly",
    "synthesis",
    "copy/paste",
    "front-load",
    "proof",
    "changed files",
    "validator results",
    "commit hash",
    "audience",
    "version",
    "release notes",
    "changelog",
    "stable baseline",
    "portfolio",
    "final package",
    "delivery intelligence"
]
REQUIRED_REPORT_PHRASES = [
    "Overlay created. Locked 175-family baseline preserved.",
    "final answer assembly",
    "priority front-loading",
    "proof integration",
    "copy/paste outputs",
    "check-result formatting",
    "audience adaptation",
    "release notes",
    "stable baseline labels",
    "portfolio/showcase delivery",
    "final package locks",
    "The Agent Command Center does not treat output as finished merely because content exists.",
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

    if data.get("extension_id") != "devinization_pack_006_output_assembly_delivery_intelligence":
        add_error(errors, "JSON: extension_id mismatch")
    if data.get("extension_name") != "Devinization Pack 6 — Output Assembly & Delivery Intelligence":
        add_error(errors, "JSON: extension_name mismatch")
    if data.get("mode") != "overlay":
        add_error(errors, "JSON: mode mismatch")
    if data.get("preserves_locked_baseline") is not True:
        add_error(errors, "JSON: preserves_locked_baseline must be true")
    if data.get("baseline_status") != "175-family expansion locked":
        add_error(errors, "JSON: baseline_status mismatch")

    if data.get("included_families") != EXPECTED_FAMILIES:
        add_error(errors, "JSON: included_families mismatch")
    if len(data.get("included_families", [])) != 2:
        add_error(errors, f"JSON: expected 2 included families, found {len(data.get('included_families', []))}")

    if data.get("delivery_layers") != EXPECTED_DELIVERY_LAYERS:
        add_error(errors, "JSON: delivery_layers mismatch")
    if len(data.get("delivery_layers", [])) != 7:
        add_error(errors, f"JSON: expected 7 delivery layers, found {len(data.get('delivery_layers', []))}")

    depends_on = data.get("depends_on", [])
    for required in ["family_007_devinized_engineering_overload", "devinization_pack_001_command_brain", "devinization_pack_002_runtime_routing_work_control", "devinization_pack_003_prompt_memory_context_architecture", "devinization_pack_004_execution_safety_tools_recovery", "devinization_pack_005_quality_standards_human_review"]:
        if required not in depends_on:
            add_error(errors, f"JSON: depends_on missing {required}")

    crews = data.get("crews", [])
    if len(crews) != 24:
        add_error(errors, f"JSON: expected 24 crews, found {len(crews)}")

    found_crews = {crew.get("crew_id"): crew.get("crew_name") for crew in crews}
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

    print("PASS: Devinization Pack 6 Output Assembly & Delivery Intelligence valid.")
    sys.exit(0)

if __name__ == "__main__":
    main()
