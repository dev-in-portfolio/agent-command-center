#!/usr/bin/env python3
import json
import os
import sys

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    family_file = os.path.join(base_dir, '02_departments', '001_agent_command', 'family.json')
    errors = []

    if not os.path.exists(family_file):
        print("FAIL")
        print(f"File not found: {family_file}")
        sys.exit(1)

    try:
        with open(family_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print("FAIL")
        print(f"Invalid JSON: {e}")
        sys.exit(1)

    if data.get("id") != 1:
        errors.append("Family id is not 1.")
    if data.get("name") != "Agent Command":
        errors.append("Family name is not 'Agent Command'.")
    if data.get("manager") != "1.M" or data.get("scribe") != "1.H" or data.get("auditor") != "1.I":
        errors.append("Manager/Scribe/Auditor fields are incorrect.")
        
    depts = data.get("departments", [])
    if not isinstance(depts, list) or len(depts) != 10:
        errors.append(f"Expected exactly 10 departments, found {len(depts) if isinstance(depts, list) else type(depts)}.")
    
    expected_roles = [
        "Realist", "Overachiever", "Dreamer", "Timid", "Overprotective",
        "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"
    ]
    role_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    
    if isinstance(depts, list):
        for i, dept in enumerate(depts, 1):
            expected_d_id = f"1.{i}"
            if dept.get("id") != expected_d_id:
                errors.append(f"Department ID expected {expected_d_id}, found {dept.get('id')}.")
            
            d_id = dept.get("id")
            if dept.get("manager") != f"{d_id}.M": errors.append(f"Manager incorrect for {d_id}")
            if dept.get("scribe") != f"{d_id}.H": errors.append(f"Scribe incorrect for {d_id}")
            if dept.get("auditor") != f"{d_id}.I": errors.append(f"Auditor incorrect for {d_id}")
            
            units = dept.get("units", [])
            if not isinstance(units, list) or len(units) != 3:
                errors.append(f"Expected 3 units in {d_id}, found {len(units) if isinstance(units, list) else type(units)}.")
            
            if isinstance(units, list):
                for j, unit in enumerate(units, 1):
                    expected_u_id = f"{d_id}.{j}"
                    if unit.get("id") != expected_u_id:
                        errors.append(f"Unit ID expected {expected_u_id}, found {unit.get('id')}.")
                    
                    u_id = unit.get("id")
                    team = unit.get("team", [])
                    if not isinstance(team, list) or len(team) != 9:
                        errors.append(f"Expected exactly 9 team roles in {u_id}, found {len(team) if isinstance(team, list) else type(team)}.")
                    
                    if isinstance(team, list):
                        for k, member in enumerate(team):
                            expected_t_id = f"{u_id}.1{role_letters[k]}"
                            if member.get("id") != expected_t_id:
                                errors.append(f"Team ID expected {expected_t_id}, found {member.get('id')}.")
                            if member.get("role") != expected_roles[k]:
                                errors.append(f"Team role expected {expected_roles[k]}, found {member.get('role')}.")

    if errors:
        print("FAIL")
        for err in errors:
            print("- " + err)
        sys.exit(1)
        
    print("PASS: Agent Command family expansion valid.")
    sys.exit(0)

if __name__ == '__main__':
    main()
