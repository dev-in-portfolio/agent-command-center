import json
import os
import sys

def main():
    json_path = "04_workflow_templates/family_007_devinized_engineering_overload_pack.json"
    report_path = "09_exports/family_007_devinized_engineering_overload_report.md"
    errors = []

    # 1. File existence
    if not os.path.exists(json_path):
        errors.append(f"File missing: {json_path}")
    if not os.path.exists(report_path):
        errors.append(f"File missing: {report_path}")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    # 2. JSON Validation
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if data.get("extension_id") != "family_007_devinized_engineering_overload":
        errors.append("JSON: extension_id mismatch")
    if data.get("base_family_id") != 7:
        errors.append("JSON: base_family_id mismatch")
    if data.get("base_family_name") != "Engineering & Automation":
        errors.append("JSON: base_family_name mismatch")
    if data.get("mode") != "overlay":
        errors.append("JSON: mode mismatch")
    if data.get("preserves_locked_baseline") is not True:
        errors.append("JSON: preserves_locked_baseline must be true")
    
    crews = data.get("crews", [])
    if len(crews) != 30:
        errors.append(f"JSON: expected 30 crews, found {len(crews)}")

    required_crews = ["7.DV.001", "7.DV.002", "7.DV.003", "7.DV.004", "7.DV.005", "7.DV.006", "7.DV.027", "7.DV.030"]
    found_crews = [c.get("crew_id") for c in crews]
    for rc in required_crews:
        if rc not in found_crews:
            errors.append(f"JSON: required crew {rc} missing")

    expected_roles = [
        "Realist", "Overachiever", "Dreamer", "Timid", "Overprotective",
        "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"
    ]

    for crew in crews:
        cid = crew.get("crew_id")
        # Check required keys
        for key in ["crew_id", "crew_name", "baseline_anchor", "mission", "triggers", "primary_outputs", "handoff_targets", "roles"]:
            if key not in crew:
                errors.append(f"Crew {cid}: missing key '{key}'")
        
        roles = crew.get("roles", [])
        if len(roles) != 9:
            errors.append(f"Crew {cid}: expected 9 roles, found {len(roles)}")
        else:
            for i, r in enumerate(roles):
                if r.get("role") != expected_roles[i]:
                    errors.append(f"Crew {cid}: role {i} mismatch. Expected '{expected_roles[i]}', found '{r.get('role')}'")
                if not r.get("id", "").startswith(cid):
                    errors.append(f"Crew {cid}: role ID mismatch for role {i}")

    # Required phrases in JSON
    json_text = json.dumps(data)
    required_json_phrases = ["Station Chief", "runnable", "work order", "deterministic demo mode", "Termux", "GitHub", "tool adapter", "portfolio", "Speed Racer", "Devinize"]
    for p in required_json_phrases:
        if p.lower() not in json_text.lower():
            errors.append(f"JSON: required phrase '{p}' missing")

    # 3. Report Validation
    with open(report_path, 'r', encoding='utf-8') as f:
        report = f.read()

    required_report_phrases = [
        "Overlay created. Locked baseline preserved.",
        "Station Chief runtime",
        "deterministic demo mode",
        "Next recommended build step"
    ]
    for p in required_report_phrases:
        if p.lower() not in report.lower():
            errors.append(f"Report: required phrase '{p}' missing")

    # 4. Manual Scope Check Notice
    print("Manual scope check required: confirm git diff contains only the three allowed files.")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    else:
        print("PASS: Family 7 Devinized Engineering Overload Pack valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()
