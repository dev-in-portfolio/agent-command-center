#!/usr/bin/env python3
import json
import os
import sys

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    spec_file = os.path.join(base_dir, '04_workflow_templates', 'family_expansion_batch_005_014.json')
    
    if not os.path.exists(spec_file):
        print(f"FAIL: Spec file not found at {spec_file}")
        sys.exit(1)
        
    with open(spec_file, 'r', encoding='utf-8') as f:
        spec = json.load(f)
        
    roles = [
        ("A", "Realist"),
        ("B", "Overachiever"),
        ("C", "Dreamer"),
        ("D", "Timid"),
        ("E", "Overprotective"),
        ("F", "Wildcard Intern"),
        ("G", "Team Lead / Manager"),
        ("H", "Scribe / Shower of Work"),
        ("I", "Auditor / Revision Director")
    ]
    
    for fam_spec in spec['families']:
        fid = fam_spec['id']
        fname = fam_spec['name']
        folder = fam_spec['folder']
        
        fam_json_path = os.path.join(base_dir, folder, 'family.json')
        readme_path = os.path.join(base_dir, folder, 'README.md')
        
        # 1. Update family.json
        if not os.path.exists(fam_json_path):
            print(f"SKIP: {fam_json_path} not found")
            continue
            
        with open(fam_json_path, 'r', encoding='utf-8') as f:
            fam_data = json.load(f)
            
        new_departments = []
        readme_depts = []
        
        for dept_spec in fam_spec['departments']:
            did = dept_spec['id']
            dname = dept_spec['name']
            
            dept_obj = {
                "id": did,
                "name": dname,
                "manager": f"{did}.M",
                "scribe": f"{did}.H",
                "auditor": f"{did}.I",
                "units": []
            }
            
            readme_depts.append(f"\n### {did} {dname}")
            
            for u_idx, uname in enumerate(dept_spec['units'], 1):
                uid = f"{did}.{u_idx}"
                unit_obj = {
                    "id": uid,
                    "name": uname,
                    "team": []
                }
                
                readme_depts.append(f"- {uid} {uname}")
                
                for r_letter, r_name in roles:
                    unit_obj["team"].append({
                        "id": f"{uid}.1{r_letter}",
                        "role": r_name
                    })
                    
                dept_obj["units"].append(unit_obj)
                
            new_departments.append(dept_obj)
            
        fam_data['departments'] = new_departments
        
        with open(fam_json_path, 'w', encoding='utf-8') as f:
            json.dump(fam_data, f, indent=2)
        print(f"WRITTEN: {fam_json_path}")
        
        # 2. Update README.md
        readme_content = f"""# {fname}

## Purpose

Placeholder purpose for {fname}.

## Family Manager ({fid}.M)

Routes family-level work, resolves escalations, and coordinates subordinate departments.

## Family Scribe ({fid}.H)

Records family-level decisions, assumptions, handoffs, and work trails.

## Family Auditor ({fid}.I)

Reviews family-level output and marks items as keep, fix, remove, redo, or escalate.

## Departments
{"".join(readme_depts)}
"""
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"WRITTEN: {readme_path}")

if __name__ == '__main__':
    main()
