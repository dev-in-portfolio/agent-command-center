import json
import os
import re
import sys

BATCH_FILE = "04_workflow_templates/family_expansion_batch_025_034.json"

HARDCODED_STRINGS = [
    "Healthcare & Wellness Division",
    "Benefits & Coverage Review",
    "Provider / Network Research",
    "Plain-Language Health Summary",
    "Real Estate & Property Division",
    "E-Commerce & Retail Division",
    "Pricing & Promotions",
    "Intellectual Property, Rights & Licensing",
    "Carbon & Impact Tracking",
    "Agent Lab & System Evolution",
    "Model Operations & AI Infrastructure",
    "Context Window Management",
    "Token & Cost Management",
    "Evaluation & Benchmarking",
    "Human Review & Approval Operations",
    "Human-in-the-Loop Control",
    "Standards, Templates & Methodology",
    "Standard Operating Standards",
    "Standards Governance"
]

def main():
    errors = []
    
    if not os.path.exists(BATCH_FILE):
        print(f"FAIL: {BATCH_FILE} not found")
        sys.exit(1)
        
    with open(BATCH_FILE, 'r', encoding='utf-8') as f:
        spec_content = f.read()
        
    # Hardcoded string checks
    for hs in HARDCODED_STRINGS:
        if hs not in spec_content:
            errors.append(f"Missing hardcoded string in spec: {hs}")
            
    spec = json.loads(spec_content)
    
    for family_spec in spec.get("families", []):
        fid = family_spec["id"]
        if not (25 <= fid <= 34):
            continue
            
        fname = family_spec["name"]
        folder = family_spec["folder"]
        family_json_path = os.path.join(folder, "family.json")
        readme_path = os.path.join(folder, "README.md")
        
        if not os.path.exists(family_json_path):
            errors.append(f"Missing file: {family_json_path}")
            continue
            
        try:
            with open(family_json_path, 'r', encoding='utf-8') as f:
                family_data = json.load(f)
        except json.JSONDecodeError:
            errors.append(f"Invalid JSON in {family_json_path}")
            continue
            
        if family_data.get("id") != fid:
            errors.append(f"Family ID mismatch in {family_json_path}: expected {fid}, got {family_data.get('id')}")
        if family_data.get("name") != fname:
            errors.append(f"Family name mismatch in {family_json_path}: expected {fname}, got {family_data.get('name')}")
            
        if family_data.get("manager") != f"{fid}.M": errors.append(f"Bad manager in {fid}")
        if family_data.get("scribe") != f"{fid}.H": errors.append(f"Bad scribe in {fid}")
        if family_data.get("auditor") != f"{fid}.I": errors.append(f"Bad auditor in {fid}")
        
        spec_depts = family_spec.get("departments", [])
        data_depts = family_data.get("departments", [])
        
        if len(data_depts) != len(spec_depts):
            errors.append(f"Dept count mismatch in {fid}: expected {len(spec_depts)}, got {len(data_depts)}")
            
        for s_dept, d_dept in zip(spec_depts, data_depts):
            did = s_dept["id"]
            if d_dept.get("id") != did:
                errors.append(f"Dept ID mismatch: expected {did}, got {d_dept.get('id')}")
            if d_dept.get("name") != s_dept["name"]:
                errors.append(f"Dept name mismatch: expected {s_dept['name']}, got {d_dept.get('name')}")
                
            if d_dept.get("manager") != f"{did}.M": errors.append(f"Bad manager in {did}")
            if d_dept.get("scribe") != f"{did}.H": errors.append(f"Bad scribe in {did}")
            if d_dept.get("auditor") != f"{did}.I": errors.append(f"Bad auditor in {did}")
            
            s_units = s_dept.get("units", [])
            d_units = d_dept.get("units", [])
            
            if len(d_units) != 3:
                errors.append(f"Dept {did} does not have exactly 3 units")
                
            for i, (s_uname, d_u) in enumerate(zip(s_units, d_units), 1):
                uid = f"{did}.{i}"
                uname = s_uname
                
                if d_u.get("id") != uid:
                    errors.append(f"Unit ID mismatch: expected {uid}, got {d_u.get('id')}")
                if d_u.get("name") != uname:
                    errors.append(f"Unit name mismatch: expected {uname}, got {d_u.get('name')}")
                    
                team = d_u.get("team", [])
                if len(team) != 9:
                    errors.append(f"Unit {uid} team size != 9")
                    
                expected_team = [
                    f"{uid}.1A Realist",
                    f"{uid}.1B Overachiever",
                    f"{uid}.1C Dreamer",
                    f"{uid}.1D Timid",
                    f"{uid}.1E Overprotective",
                    f"{uid}.1F Wildcard Intern",
                    f"{uid}.1G Team Lead / Manager",
                    f"{uid}.1H Scribe / Shower of Work",
                    f"{uid}.1I Auditor / Revision Director"
                ]
                
                if team != expected_team:
                    errors.append(f"Unit {uid} team mismatch")
                    
        # Validate README
        if not os.path.exists(readme_path):
            errors.append(f"Missing README: {readme_path}")
        else:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                
            for line in readme_content.splitlines():
                if line.startswith("###") and re.search(r"-\s*\d+\.\d+\.\d+", line):
                    errors.append(f"Squished heading/bullet in {readme_path}")
                
            for s_dept in spec_depts:
                did = s_dept["id"]
                dname = s_dept["name"]
                expected_heading = f"### {did} {dname}"
                if expected_heading not in readme_content:
                    errors.append(f"Missing heading {expected_heading} in {readme_path}")
                    
                for i, s_uname in enumerate(s_dept.get("units", []), 1):
                    uid = f"{did}.{i}"
                    expected_bullet = f"- {uid} {s_uname}"
                    if expected_bullet not in readme_content:
                        errors.append(f"Missing bullet {expected_bullet} in {readme_path}")

    if errors:
        for e in errors:
            print(e)
        print("FAIL")
        sys.exit(1)
        
    print("PASS: Family batch 025-034 expansion valid.")
    sys.exit(0)

if __name__ == "__main__":
    main()
