import json
import os
import sys
import re

def validate_full_completion():
    errors = []
    
    # 1. dashboard_seed.json
    dashboard_path = "09_exports/dashboard_seed.json"
    if not os.path.exists(dashboard_path):
        errors.append(f"File missing: {dashboard_path}")
    else:
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            dashboard_data = json.load(f)
        
        families = dashboard_data.get("families", [])
        if len(families) != 175:
            errors.append(f"Dashboard count mismatch: expected 175, found {len(families)}")
            
        # GAP 1: Verify family IDs are exactly 1 through 175
        dashboard_ids = sorted(entry.get("id") for entry in families)
        expected_ids = list(range(1, 176))
        if dashboard_ids != expected_ids:
            errors.append(f"Dashboard family IDs mismatch: expected 1 through 175, found {dashboard_ids}")

        for entry in families:
            fid = entry.get("id")
            status = entry.get("status")
            if not isinstance(fid, int):
                errors.append(f"Dashboard entry ID {fid} is not an integer")
            if status != "expanded":
                errors.append(f"Dashboard family {fid} status is '{status}', expected 'expanded'")

    # 2. master_department_list.md
    md_list_path = "09_exports/master_department_list.md"
    if not os.path.exists(md_list_path):
        errors.append(f"File missing: {md_list_path}")
    else:
        with open(md_list_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        matches = re.findall(r"^\d+\.", content, re.MULTILINE)
        if len(matches) != 175:
            errors.append(f"Master list numbering mismatch: expected 175 items, found {len(matches)}")
            
        if "1. Agent Command" not in content:
            errors.append("Master list missing '1. Agent Command'")
        if "175. Master Archive / Library of Alexandria" not in content:
            errors.append("Master list missing '175. Master Archive / Library of Alexandria'")

    # 3. family.json and README.md files
    if 'families' in locals():
        for entry in families:
            fid = entry.get("id")
            fname = entry.get("label")
            fdir = entry.get("folder")
            
            if not fdir or not os.path.exists(fdir):
                errors.append(f"Folder missing or undefined for family {fid}: {fdir}")
                continue
                
            # family.json validation
            fjson_path = os.path.join(fdir, "family.json")
            if not os.path.exists(fjson_path):
                errors.append(f"family.json missing: {fjson_path}")
            else:
                with open(fjson_path, 'r', encoding='utf-8') as f:
                    fjson = json.load(f)
                
                if not isinstance(fjson.get("id"), int):
                    errors.append(f"ID in {fjson_path} is not an integer")
                elif fjson.get("id") != fid:
                    errors.append(f"ID mismatch in {fjson_path}: expected {fid}, found {fjson.get('id')}")
                    
                if fjson.get("name") != fname:
                    errors.append(f"Name mismatch in {fjson_path}: expected '{fname}', found '{fjson.get('name')}'")
                
                if fjson.get("manager") != f"{fid}.M": errors.append(f"Manager mismatch in {fjson_path}")
                if fjson.get("scribe") != f"{fid}.H": errors.append(f"Scribe mismatch in {fjson_path}")
                if fjson.get("auditor") != f"{fid}.I": errors.append(f"Auditor mismatch in {fjson_path}")
                
                depts = fjson.get("departments", [])
                if not depts:
                    errors.append(f"Departments array empty or missing in {fjson_path}")
                # GAP 2: Exactly 10 departments
                elif len(depts) != 10:
                    errors.append(f"Department count for family {fid} is {len(depts)}, expected exactly 10")
                    
                for dept in depts:
                    did = dept.get("id")
                    if not did:
                        errors.append(f"Missing ID for department in {fjson_path}")
                        continue
                    if dept.get("manager") != f"{did}.M": errors.append(f"Manager mismatch for dept {did}")
                    if dept.get("scribe") != f"{did}.H": errors.append(f"Scribe mismatch for dept {did}")
                    if dept.get("auditor") != f"{did}.I": errors.append(f"Auditor mismatch for dept {did}")
                    
                    units = dept.get("units", [])
                    if len(units) != 3:
                        errors.append(f"Unit count for dept {did} is {len(units)}, expected 3")
                        
                    for unit in units:
                        uid = unit.get("id")
                        if not uid:
                            errors.append(f"Missing ID for unit in dept {did}")
                            continue
                        
                        team = unit.get("team", [])
                        if len(team) != 9:
                            errors.append(f"Team count for unit {uid} is {len(team)}, expected 9")
                            
                        roles = [
                            "Realist", "Overachiever", "Dreamer", "Timid", "Overprotective",
                            "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work",
                            "Auditor / Revision Director"
                        ]
                        suffixes = ["1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H", "1I"]
                        
                        for i, member in enumerate(team):
                            if not isinstance(member, dict):
                                errors.append(f"Team member in unit {uid} is not a dict")
                                continue
                            expected_id = f"{uid}.{suffixes[i]}"
                            expected_role = roles[i]
                            if member.get("id") != expected_id:
                                errors.append(f"Team ID mismatch in {uid}: expected {expected_id}, found {member.get('id')}")
                            if member.get("role") != expected_role:
                                errors.append(f"Role mismatch in {uid}: expected {expected_role}, found {member.get('role')}")

            # README.md validation
            readme_path = os.path.join(fdir, "README.md")
            if not os.path.exists(readme_path):
                errors.append(f"README.md missing: {readme_path}")
            else:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme = f.read()
                
                if not readme.startswith(f"# {fname}"):
                    errors.append(f"README {fid} title mismatch or bad start")
                if "## Purpose" not in readme: errors.append(f"README {fid} missing Purpose")
                if f"## Family Manager ({fid}.M)" not in readme: errors.append(f"README {fid} missing Manager section")
                if f"## Family Scribe ({fid}.H)" not in readme: errors.append(f"README {fid} missing Scribe section")
                if f"## Family Auditor ({fid}.I)" not in readme: errors.append(f"README {fid} missing Auditor section")
                if "## Departments" not in readme: errors.append(f"README {fid} missing Departments section")
                
                # Check for incorrect formatting
                if re.search(r"### .* \(\d+\.\d+\)", readme):
                    errors.append(f"README {fid} uses forbidden '### Name (ID)' format")
                if re.search(r"- .* \(\d+\.\d+\.\d+\)", readme):
                    errors.append(f"README {fid} uses forbidden '- Name (ID)' format")
                
                # Check for correct formatting
                if 'fjson' in locals() and "departments" in fjson:
                    for dept in fjson["departments"]:
                        expected_h3 = f"### {dept['id']} {dept['name']}"
                        if expected_h3 not in readme:
                            errors.append(f"README {fid} missing correct dept heading: '{expected_h3}'")
                        for unit in dept["units"]:
                            expected_bullet = f"- {unit['id']} {unit['name']}"
                            if expected_bullet not in readme:
                                errors.append(f"README {fid} missing correct unit bullet: '{expected_bullet}'")

    # 4. org_chart_export.json
    org_chart_path = "09_exports/org_chart_export.json"
    if not os.path.exists(org_chart_path):
        errors.append(f"File missing: {org_chart_path}")
    else:
        with open(org_chart_path, 'r', encoding='utf-8') as f:
            org_chart = f.read()
        
        required_terms = [
            '"id": 1,',
            '"id": 175,',
            "Master Archive / Library of Alexandria",
            "Master Archive Dashboard",
            "Library Status Summary"
        ]
        for term in required_terms:
            if term not in org_chart:
                errors.append(f"org_chart_export.json missing required term: '{term}'")

    if errors:
        for error in errors:
            print(error)
        print("FAIL")
        sys.exit(1)
    else:
        print("PASS: Full 175-family expansion complete.")

if __name__ == "__main__":
    validate_full_completion()
