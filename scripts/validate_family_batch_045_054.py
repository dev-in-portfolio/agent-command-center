import json
import os
import sys
import re

SPEC_PATH = '04_workflow_templates/family_expansion_batch_045_054.json'

HARDCODED_STRINGS = [
    "Recruiting, Career & Professional Positioning",
    "Resume Strategy",
    "Professional Proof Assets",
    "Portfolio, Case Studies & Proof Assets",
    "Capabilities Page Management",
    "Recruiter-Facing Packaging",
    "Personal Productivity & Time Management",
    "Procrastination Recovery",
    "Completion Rituals",
    "Life Administration",
    "Emergency Information",
    "Life Admin Dashboard",
    "Personal Knowledge, Learning & Skill Building",
    "Skill Transfer",
    "Creative Studio & Story Worlds",
    "Series Bible Management",
    "Brand, Identity & Personal Mythology",
    "Personal Mythology",
    "Personal AI Companion Architecture",
    "Companion Personality Design",
    "Prompt Systems & Instruction Architecture",
    "Instruction Hierarchy",
    "Memory Engineering & Context Architecture",
    "Cross-Thread Continuity",
    "Memory Governance"
]

def validate():
    errors = []
    
    if not os.path.exists(SPEC_PATH):
        print(f"FAIL: {SPEC_PATH} not found")
        sys.exit(1)
        
    with open(SPEC_PATH, 'r', encoding='utf-8') as f:
        spec_content = f.read()
        spec = json.loads(spec_content)
        
    # hardcoded prompt-fidelity checks
    for s in HARDCODED_STRINGS:
        if s not in spec_content:
            errors.append(f"Missing hardcoded string in spec: {s}")
            
    for family in spec['families']:
        fid = family['id']
        fname = family['name']
        folder = family['folder']
        
        family_json_path = os.path.join(folder, 'family.json')
        readme_path = os.path.join(folder, 'README.md')
        
        if not os.path.exists(family_json_path):
            errors.append(f"Missing file: {family_json_path}")
            continue
            
        with open(family_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if data.get('id') != fid: errors.append(f"Family ID mismatch in {family_json_path}")
        if data.get('name') != fname: errors.append(f"Family Name mismatch in {family_json_path}")
        if data.get('manager') != f"{fid}.M": errors.append(f"Family Manager mismatch in {family_json_path}")
        if data.get('scribe') != f"{fid}.H": errors.append(f"Family Scribe mismatch in {family_json_path}")
        if data.get('auditor') != f"{fid}.I": errors.append(f"Family Auditor mismatch in {family_json_path}")
        
        depts = data.get('departments', [])
        if len(depts) != len(family['departments']):
            errors.append(f"Dept count mismatch in {family_json_path}")
            
        for i, dept_spec in enumerate(family['departments']):
            if i >= len(depts): break
            dept_data = depts[i]
            did = dept_spec['id']
            dname = dept_spec['name']
            
            if dept_data.get('id') != did: errors.append(f"Dept ID mismatch: {did}")
            if dept_data.get('name') != dname: errors.append(f"Dept Name mismatch: {did}")
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
                
                if unit_data.get('id') != uid: errors.append(f"Unit ID mismatch: {uid}")
                if unit_data.get('name') != unit_name: errors.append(f"Unit Name mismatch: {uid}")
                
                team = unit_data.get('team', [])
                if len(team) != 9:
                    errors.append(f"Team size mismatch in unit {uid}")
                    
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
            
            for dept_spec in family['departments']:
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
        print("PASS: Family batch 045-054 expansion valid.")
        sys.exit(0)

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    validate()
