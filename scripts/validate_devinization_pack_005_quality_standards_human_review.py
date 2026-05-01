import json
import os
import sys

JSON_PATH = "04_workflow_templates/devinization_pack_005_quality_standards_human_review.json"
REPORT_PATH = "09_exports/devinization_pack_005_quality_standards_human_review_report.md"
EXPECTED_FAMILIES = [
    {
        "family_id": 8,
        "family_name": "Quality, Risk & Compliance"
    },
    {
        "family_id": 32,
        "family_name": "Evaluation & Benchmarking"
    },
    {
        "family_id": 33,
        "family_name": "Human Review & Approval Operations"
    },
    {
        "family_id": 34,
        "family_name": "Standards, Templates & Methodology"
    },
    {
        "family_id": 95,
        "family_name": "Compliance Evidence, Attestation & Regulated Deliverables"
    },
    {
        "family_id": 128,
        "family_name": "Work Product Governance & Deliverable Standards"
    },
    {
        "family_id": 129,
        "family_name": "Knowledge Quality, Currency & Source Freshness"
    },
    {
        "family_id": 131,
        "family_name": "Approval UX, Review Queues & Human Control"
    }
]
EXPECTED_QUALITY_REVIEW_LAYERS = [
    {
        "layer": 1,
        "name": "Quality Gate",
        "purpose": "Check whether the work satisfies the objective, avoids obvious defects, and meets the expected standard before review."
    },
    {
        "layer": 2,
        "name": "Standards & Template Gate",
        "purpose": "Ensure outputs follow the correct format, template, naming convention, structure, tone, and methodology."
    },
    {
        "layer": 3,
        "name": "Evidence & Source Gate",
        "purpose": "Verify that factual claims, citations, source freshness, proof artifacts, and regulated evidence are adequate."
    },
    {
        "layer": 4,
        "name": "Risk & Compliance Gate",
        "purpose": "Identify compliance, safety, legal, privacy, reputation, and business risks before delivery."
    },
    {
        "layer": 5,
        "name": "Human Review Gate",
        "purpose": "Route work to human review when judgment, approval, sensitive action, or final signoff is required."
    },
    {
        "layer": 6,
        "name": "Benchmark & Evaluation Gate",
        "purpose": "Compare outputs against rubrics, benchmarks, prior versions, known-good examples, and measurable criteria."
    },
    {
        "layer": 7,
        "name": "Deliverable Governance Gate",
        "purpose": "Confirm the work product is complete, usable, labeled, versioned, and ready for the intended audience."
    },
    {
        "layer": 8,
        "name": "Approval UX Gate",
        "purpose": "Present review decisions, approval choices, change requests, and final control points clearly to the human operator."
    }
]
EXPECTED_CREWS = [
    [
        "DV.P5.001",
        "Quality Gate Crew"
    ],
    [
        "DV.P5.002",
        "Risk Review Crew"
    ],
    [
        "DV.P5.003",
        "Compliance Screen Crew"
    ],
    [
        "DV.P5.004",
        "Accuracy Review Crew"
    ],
    [
        "DV.P5.005",
        "Quality Failure Repair Crew"
    ],
    [
        "DV.P5.006",
        "Final Quality Signoff Crew"
    ],
    [
        "DV.P5.007",
        "Evaluation Rubric Crew"
    ],
    [
        "DV.P5.008",
        "Benchmark Comparison Crew"
    ],
    [
        "DV.P5.009",
        "Regression Benchmark Crew"
    ],
    [
        "DV.P5.010",
        "Evaluation Evidence Crew"
    ],
    [
        "DV.P5.011",
        "Agent Performance Review Crew"
    ],
    [
        "DV.P5.012",
        "Evaluation Failure Crew"
    ],
    [
        "DV.P5.013",
        "Human Review Routing Crew"
    ],
    [
        "DV.P5.014",
        "Review Packet Assembly Crew"
    ],
    [
        "DV.P5.015",
        "Human Feedback Capture Crew"
    ],
    [
        "DV.P5.016",
        "Review Escalation Crew"
    ],
    [
        "DV.P5.017",
        "Approval Boundary Crew"
    ],
    [
        "DV.P5.018",
        "Review Closure Crew"
    ],
    [
        "DV.P5.019",
        "Standards Registry Crew"
    ],
    [
        "DV.P5.020",
        "Template Contract Crew"
    ],
    [
        "DV.P5.021",
        "Methodology Selection Crew"
    ],
    [
        "DV.P5.022",
        "Methodology QA Crew"
    ],
    [
        "DV.P5.023",
        "Template Compliance Crew"
    ],
    [
        "DV.P5.024",
        "Reusable Standard Crew"
    ],
    [
        "DV.P5.025",
        "Evidence Requirement Crew"
    ],
    [
        "DV.P5.026",
        "Evidence Collection Crew"
    ],
    [
        "DV.P5.027",
        "Attestation Crew"
    ],
    [
        "DV.P5.028",
        "Regulated Language Crew"
    ],
    [
        "DV.P5.029",
        "Disclaimer & Scope Note Crew"
    ],
    [
        "DV.P5.030",
        "Regulated Deliverable Review Crew"
    ],
    [
        "DV.P5.031",
        "Source Freshness Crew"
    ],
    [
        "DV.P5.032",
        "Knowledge Currency Crew"
    ],
    [
        "DV.P5.033",
        "Citation Integrity Crew"
    ],
    [
        "DV.P5.034",
        "Knowledge Confidence Crew"
    ],
    [
        "DV.P5.035",
        "Source Gap Crew"
    ],
    [
        "DV.P5.036",
        "Freshness Lock Crew"
    ],
    [
        "DV.P5.037",
        "Deliverable Readiness Crew"
    ],
    [
        "DV.P5.038",
        "Version / Label Governance Crew"
    ],
    [
        "DV.P5.039",
        "Packaging Standard Crew"
    ],
    [
        "DV.P5.040",
        "Governance Feedback Crew"
    ],
    [
        "DV.P5.041",
        "Work Product Archive Crew"
    ],
    [
        "DV.P5.042",
        "Deliverable Defect Crew"
    ],
    [
        "DV.P5.043",
        "Review Queue Intake Crew"
    ],
    [
        "DV.P5.044",
        "Approval Risk Flag Crew"
    ],
    [
        "DV.P5.045",
        "Approval Decision Crew"
    ],
    [
        "DV.P5.046",
        "Approval Record Crew"
    ],
    [
        "DV.P5.047",
        "Change Request Crew"
    ],
    [
        "DV.P5.048",
        "Human Control Lock Crew"
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
    "quality gate",
    "risk review",
    "compliance",
    "benchmark",
    "human review",
    "approval queue",
    "standards",
    "template",
    "evidence",
    "attestation",
    "regulated deliverable",
    "source freshness",
    "citation integrity",
    "deliverable readiness",
    "approval UX",
    "human-control",
    "ready to ship",
    "quality checked"
]
REQUIRED_REPORT_PHRASES = [
    "Overlay created. Locked 175-family baseline preserved.",
    "quality gates",
    "risk review",
    "compliance screening",
    "evaluation rubrics",
    "human review routing",
    "evidence requirements",
    "source freshness checks",
    "citation integrity checks",
    "deliverable readiness review",
    "human-control locks",
    "The Agent Command Center does not treat “created” as “quality checked.”",
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

    if data.get("extension_id") != "devinization_pack_005_quality_standards_human_review":
        add_error(errors, "JSON: extension_id mismatch")
    if data.get("extension_name") != "Devinization Pack 5 — Quality, Standards & Human Review":
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

    if data.get("quality_review_layers") != EXPECTED_QUALITY_REVIEW_LAYERS:
        add_error(errors, "JSON: quality_review_layers mismatch")
    if len(data.get("quality_review_layers", [])) != 8:
        add_error(errors, f"JSON: expected 8 quality review layers, found {len(data.get('quality_review_layers', []))}")

    depends_on = data.get("depends_on", [])
    for required in ["family_007_devinized_engineering_overload", "devinization_pack_001_command_brain", "devinization_pack_002_runtime_routing_work_control", "devinization_pack_003_prompt_memory_context_architecture", "devinization_pack_004_execution_safety_tools_recovery"]:
        if required not in depends_on:
            add_error(errors, f"JSON: depends_on missing {required}")

    crews = data.get("crews", [])
    if len(crews) != 48:
        add_error(errors, f"JSON: expected 48 crews, found {len(crews)}")

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

    print("PASS: Devinization Pack 5 Quality, Standards & Human Review valid.")
    sys.exit(0)

if __name__ == "__main__":
    main()
