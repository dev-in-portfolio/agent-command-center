import json
import os
import sys
import re

# Ensure we are in project root
project_root = os.getcwd()
if os.path.basename(project_root) == 'scripts':
    os.chdir('..')

SPEC_PATH = '04_workflow_templates/family_expansion_batch_095_104.json'

HARDCODED_STRINGS = [
    "Compliance Evidence, Attestation & Regulated Deliverables",
    "Regulated Deliverable Review",
    "Required Language Control",
    "Digital Asset Management & Creative Libraries",
    "Rights And Usage Tracking",
    "Creative Library Dashboard",
    "Forms, Intake & Structured Data Collection",
    "Structured Data Export",
    "Form Compliance Review",
    "Inbox, Notifications & Signal Management",
    "Signal Extraction",
    "Digest Creation",
    "Calendar, Scheduling & Time Intelligence",
    "Deadline Forecasting",
    "Time Intelligence Dashboard",
    "Master Control, Meta-Architecture & System Constitution",
    "System Constitution",
    "Constitutional Changelog",
    "Cross-Project Intelligence & Pattern Transfer",
    "Project Memory Bridging",
    "Cross-Project Risk Detection",
    "Error Recovery, Apology & Repair Systems",
    "Apology Design",
    "User Frustration Recovery",
    "Attention Management & Cognitive Workspace",
    "Context Stack Control",
    "Cognitive Parking Lot",
    "User Intent Forensics",
    "Hidden Constraint Detection",
    "Intent Evidence Trace"
]

def validate():
    errors = []
    
    if not os.path.exists(SPEC_PATH):
        print(f"FAIL: {SPEC_PATH} not found")
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
                data = json.load(f)
            except json.JSONDecodeError:
                errors.append(f"Invalid JSON in {family_json_path}")
                continue
            
        if data.get('id') != fid: errors.append(f"Family ID mismatch in {family_json_path}: expected {fid}, got {data.get('id')}")
        if data.get('name') != fname: errors.append(f"Family Name mismatch in {family_json_path}: expected {fname}, got {data.get('name')}")
        if data.get('manager') != f"{fid}.M": errors.append(f"Family Manager mismatch in {family_json_path}")
        if data.get('scribe') != f"{fid}.H": errors.append(f"Family Scribe mismatch in {family_json_path}")
        if data.get('auditor') != f"{fid}.I": errors.append(f"Family Auditor mismatch in {family_json_path}")
        
        depts = data.get('departments', [])
        if len(depts) != len(family_spec['departments']):
            errors.append(f"Dept count mismatch in {family_json_path}")
            
        for i, dept_spec in enumerate(family_spec['departments']):
            if i >= len(depts): break
            dept_data = depts[i]
            did = dept_spec['id']
            dname = dept_spec['name']
            
            if dept_data.get('id') != did: errors.append(f"Dept ID mismatch: expected {did}, got {dept_data.get('id')}")
            if dept_data.get('name') != dname: errors.append(f"Dept Name mismatch: expected {dname}, got {dept_data.get('name')}")
            if dept_data.get('manager') != f"{did}.M": errors.append(f"Dept Manager mismatch: {did}")
            if dept_data.get('scribe') != f"{did}.H": errors.append(f"Dept Scribe mismatch: {did}")
            if dept_data.get('auditor') != f"{did}.I": errors.append(f"Dept Auditor mismatch: {did}")
            
            units = dept_data.get('units', [])
            if len(units) != len(dept_spec['units']):
                errors.append(f"Unit count mismatch in dept {did}")
                
            for j, unit_name in enumerate(dept_spec['units']):
                if j >= len(units): break
                unit_data = units[j]
                uid = f"{did}.{j+1}"
                
                if unit_data.get('id') != uid: errors.append(f"Unit ID mismatch: expected {uid}, got {unit_data.get('id')}")
                if unit_data.get('name') != unit_name: errors.append(f"Unit Name mismatch: expected {unit_name}, got {unit_data.get('name')}")
                
                team = unit_data.get('team', [])
                if len(team) != 9:
                    errors.append(f"Team size mismatch in unit {uid}: expected 9, got {len(team)}")
                    
                role_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
                role_names = [
                    "Realist", "Overachiever", "Dreamer", "Timid", "Overprotective",
                    "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"
                ]
                
                for k, member in enumerate(team):
                    if k >= 9: break
                    if not isinstance(member, dict):
                        errors.append(f"Team member is not an object in unit {uid} at index {k}")
                        continue
                    
                    expected_id = f"{uid}.1{role_letters[k]}"
                    expected_role = role_names[k]
                    
                    if member.get('id') != expected_id:
                        errors.append(f"Team ID mismatch in unit {uid}: expected {expected_id}, got {member.get('id')}")
                    if member.get('role') != expected_role:
                        errors.append(f"Team Role mismatch in unit {uid}: expected {expected_role}, got {member.get('role')}")

        # Validate README
        if not os.path.exists(readme_path):
            errors.append(f"Missing README: {readme_path}")
        else:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                
            # Squished heading/bullet check
            for line in readme_content.splitlines():
                if line.startswith("###") and re.search(r"-\s*\d+\.\d+\.\d+", line):
                    errors.append(f"Squished heading/bullet in {readme_path}: {line}")
            
            for dept_spec in family_spec['departments']:
                if f"### {dept_spec['id']} {dept_spec['name']}" not in readme_content:
                    errors.append(f"Missing dept heading in {readme_path}: {dept_spec['id']}")
                for j, unit_name in enumerate(dept_spec['units'], 1):
                    uid = f"{dept_spec['id']}.{j}"
                    if f"- {uid} {unit_name}" not in readme_content:
                        errors.append(f"Missing unit bullet in {readme_path}: {uid}")

    if errors:
        for err in errors:
            print(f"Error: {err}")
        print("FAIL")
        sys.exit(1)
    else:
        print("PASS: Family batch 095-104 expansion valid.")
        sys.exit(0)

if __name__ == "__main__":
    validate()
