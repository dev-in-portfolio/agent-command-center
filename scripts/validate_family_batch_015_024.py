#!/usr/bin/env python3
import json
import os
import sys

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    spec_file = os.path.join(base_dir, '04_workflow_templates', 'family_expansion_batch_015_024.json')
    
    if not os.path.exists(spec_file):
        print(f"FAIL: Spec file not found at {spec_file}")
        sys.exit(1)
        
    with open(spec_file, 'r', encoding='utf-8') as f:
        spec = json.load(f)
        
    errors = []
    
    expected_roles = [
        "Realist", "Overachiever", "Dreamer", "Timid", "Overprotective",
        "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"
    ]
    role_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

    for fam_spec in spec['families']:
        fid = fam_spec['id']
        fname = fam_spec['name']
        folder = fam_spec['folder']
        
        fam_json_path = os.path.join(base_dir, folder, 'family.json')
        readme_path = os.path.join(base_dir, folder, 'README.md')
        
        if not os.path.exists(fam_json_path):
            errors.append(f"Family file not found: {fam_json_path}")
            continue
            
        try:
            with open(fam_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            errors.append(f"Invalid JSON in {fam_json_path}: {e}")
            continue
            
        if data.get("id") != fid: errors.append(f"Family {fid} id mismatch: {data.get('id')}")
        if data.get("name") != fname: errors.append(f"Family {fid} name mismatch: {data.get('name')}")
        if data.get("manager") != f"{fid}.M": errors.append(f"Family {fid} manager mismatch")
        if data.get("scribe") != f"{fid}.H": errors.append(f"Family {fid} scribe mismatch")
        if data.get("auditor") != f"{fid}.I": errors.append(f"Family {fid} auditor mismatch")
        
        depts = data.get("departments", [])
        if len(depts) != len(fam_spec['departments']):
            errors.append(f"Family {fid} department count mismatch: expected {len(fam_spec['departments'])}, found {len(depts)}")
            
        for i, dept in enumerate(depts):
            if i >= len(fam_spec['departments']): break
            dspec = fam_spec['departments'][i]
            did = dspec['id']
            dname = dspec['name']
            
            if dept.get("id") != did: errors.append(f"Dept {did} id mismatch")
            if dept.get("name") != dname: errors.append(f"Dept {did} name mismatch")
            if dept.get("manager") != f"{did}.M": errors.append(f"Dept {did} manager mismatch")
            if dept.get("scribe") != f"{did}.H": errors.append(f"Dept {did} scribe mismatch")
            if dept.get("auditor") != f"{did}.I": errors.append(f"Dept {did} auditor mismatch")
            
            units = dept.get("units", [])
            if len(units) != len(dspec['units']):
                errors.append(f"Dept {did} unit count mismatch: expected {len(dspec['units'])}, found {len(units)}")
                
            for j, unit in enumerate(units):
                if j >= len(dspec['units']): break
                uname = dspec['units'][j]
                uid = f"{did}.{j+1}"
                
                if unit.get("id") != uid: errors.append(f"Unit {uid} id mismatch")
                if unit.get("name") != uname: errors.append(f"Unit {uid} name mismatch")
                
                team = unit.get("team", [])
                if len(team) != 9:
                    errors.append(f"Unit {uid} team size mismatch: {len(team)}")
                else:
                    for k, member in enumerate(team):
                        expected_t_id = f"{uid}.1{role_letters[k]}"
                        if member.get("id") != expected_t_id:
                            errors.append(f"Team ID mismatch at {uid}: expected {expected_t_id}, found {member.get('id')}")
                        if member.get("role") != expected_roles[k]:
                            errors.append(f"Team role mismatch at {uid}: expected {expected_roles[k]}, found {member.get('role')}")

        # Validate README formatting
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                
            if "###" in readme_content and "-" in readme_content:
                import re
                for line in readme_content.splitlines():
                    # Check for "### Heading- 1.1.1 Bullet" pattern
                    if line.startswith("###") and re.search(r"-\s*\d+\.\d+\.\d+", line):
                        errors.append(f"README at {readme_path} contains squished heading/bullet: {line}")
                        
            # Check all headings and bullets exist
            for dspec in fam_spec['departments']:
                if f"### {dspec['id']} {dspec['name']}" not in readme_content:
                    errors.append(f"README at {readme_path} missing heading for {dspec['id']}")
                for j, uname in enumerate(dspec['units'], 1):
                    uid = f"{dspec['id']}.{j}"
                    if f"- {uid} {uname}" not in readme_content:
                        errors.append(f"README at {readme_path} missing bullet for {uid}")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    else:
        print("PASS: Family batch 015-024 expansion valid.")
        sys.exit(0)

if __name__ == '__main__':
    main()
