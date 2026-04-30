import json
import os
import sys
import re

SPEC_PATH = '04_workflow_templates/family_expansion_batch_035_044.json'

HARDCODED_STRINGS = [
    "Workflow Control Tower",
    "Central Intake & Dispatch",
    "Deadline & SLA Tracking",
    "Regulatory Monitoring & Change Intelligence",
    "Plain-Language Rule Summary",
    "Knowledge Security & Information Classification",
    "Data Leakage Prevention",
    "Simulation, Forecasting & Decision Games",
    "Monte Carlo Style Reasoning",
    "Negotiation & Deal Desk",
    "Contract Term Support",
    "Reputation, Trust & Brand Risk",
    "Trust Repair",
    "Customer Insight & Voice of Customer",
    "Voice of Customer Capture",
    "Offer Design & Productized Services",
    "Productized Workflow",
    "Knowledge Products & Course Production",
    "Digital Download Packaging",
    "Talent Marketplace & Freelance Operations",
    "Payment & Milestone Review"
]

def validate_expansion():
    errors = []
    
    if not os.path.exists(SPEC_PATH):
        print(f"FAIL: Spec file not found at {SPEC_PATH}")
        sys.exit(1)

    with open(SPEC_PATH, 'r', encoding='utf-8') as f:
        spec_content = f.read()
        spec = json.loads(spec_content)

    # Hardcoded string checks
    for s in HARDCODED_STRINGS:
        if s not in spec_content:
            errors.append(f"Missing hardcoded string in spec: {s}")

    for family_spec in spec['families']:
        fid = family_spec['id']
        fname = family_spec['name']
        folder = family_spec['folder']
        
        family_json_path = os.path.join(folder, 'family.json')
        readme_path = os.path.join(folder, 'README.md')
        
        if not os.path.exists(family_json_path):
            errors.append(f"Missing file: {family_json_path}")
            continue
            
        with open(family_json_path, 'r', encoding='utf-8') as f:
            try:
                family_data = json.load(f)
            except json.JSONDecodeError:
                errors.append(f"Invalid JSON: {family_json_path}")
                continue

        if family_data.get('id') != fid:
            errors.append(f"Family ID mismatch for {folder}: expected {fid}, got {family_data.get('id')}")
        if family_data.get('name') != fname:
            errors.append(f"Family name mismatch for {folder}: expected {fname}, got {family_data.get('name')}")
        
        if family_data.get('manager') != f"{fid}.M":
            errors.append(f"Family manager mismatch for {folder}")
        if family_data.get('scribe') != f"{fid}.H":
            errors.append(f"Family scribe mismatch for {folder}")
        if family_data.get('auditor') != f"{fid}.I":
            errors.append(f"Family auditor mismatch for {folder}")

        depts = family_data.get('departments', [])
        if len(depts) != len(family_spec['departments']):
            errors.append(f"Department count mismatch for {folder}")
            
        for i, dept_spec in enumerate(family_spec['departments']):
            if i >= len(depts): break
            dept_data = depts[i]
            did = dept_spec['id']
            dname = dept_spec['name']
            
            if dept_data.get('id') != did:
                errors.append(f"Dept ID mismatch: {did}")
            if dept_data.get('name') != dname:
                errors.append(f"Dept name mismatch: {did}")
            
            if dept_data.get('manager') != f"{did}.M":
                errors.append(f"Dept manager mismatch: {did}")
            if dept_data.get('scribe') != f"{did}.H":
                errors.append(f"Dept scribe mismatch: {did}")
            if dept_data.get('auditor') != f"{did}.I":
                errors.append(f"Dept auditor mismatch: {did}")
                
            units = dept_data.get('units', [])
            if len(units) != len(dept_spec['units']):
                errors.append(f"Unit count mismatch for dept {did}")
                
            for j, unit_name_spec in enumerate(dept_spec['units']):
                if j >= len(units): break
                unit_data = units[j]
                uid = f"{did}.{j+1}"
                
                if unit_data.get('id') != uid:
                    errors.append(f"Unit ID mismatch: {uid}")
                if unit_data.get('name') != unit_name_spec:
                    errors.append(f"Unit name mismatch: {uid}")
                    
                team = unit_data.get('team', [])
                if len(team) != 9:
                    errors.append(f"Team size mismatch for unit {uid}")
                    
                expected_roles = [
                    "Realist", "Overachiever", "Dreamer", "Timid", "Overprotective",
                    "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"
                ]
                role_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
                
                for k, member in enumerate(team):
                    if not isinstance(member, dict):
                        errors.append(f"Team member is not an object for unit {uid} at index {k}")
                        continue
                    
                    expected_id = f"{uid}.1{role_letters[k]}"
                    expected_role = expected_roles[k]
                    
                    if member.get('id') != expected_id:
                        errors.append(f"Member ID mismatch for unit {uid}: expected {expected_id}, got {member.get('id')}")
                    if member.get('role') != expected_role:
                        errors.append(f"Member role mismatch for unit {uid}: expected {expected_role}, got {member.get('role')}")

        # Validate README
        if not os.path.exists(readme_path):
            errors.append(f"Missing README: {readme_path}")
        else:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                
            # Check for squished heading and bullet
            for line in readme_content.splitlines():
                if line.startswith("###") and re.search(r"-\s*\d+\.\d+\.\d+", line):
                    errors.append(f"Squished heading/bullet in {readme_path}: {line}")
                
            for dept_spec in family_spec['departments']:
                if f"### {dept_spec['id']} {dept_spec['name']}" not in readme_content:
                    errors.append(f"Missing heading for dept {dept_spec['id']} in README")
                for j, unit_name in enumerate(dept_spec['units'], 1):
                    uid = f"{dept_spec['id']}.{j}"
                    if f"- {uid} {unit_name}" not in readme_content:
                        errors.append(f"Missing bullet for unit {uid} in README")

    if errors:
        for err in errors:
            print(f"Error: {err}")
        print("FAIL")
        sys.exit(1)
    else:
        print("PASS: Family batch 035-044 expansion valid.")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    validate_expansion()
