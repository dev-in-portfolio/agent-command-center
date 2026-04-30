#!/usr/bin/env python3
import json
import os
import sys

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    
    registry_file = os.path.join(base_dir, '01_registry', 'department_families.json')
    org_chart_file = os.path.join(base_dir, '09_exports', 'org_chart_export.json')
    dashboard_file = os.path.join(base_dir, '09_exports', 'dashboard_seed.json')
    md_file = os.path.join(base_dir, '09_exports', 'master_department_list.md')
    
    errors = []

    # Read registry
    try:
        with open(registry_file, 'r', encoding='utf-8') as f:
            registry = json.load(f)
            registry_names = {item['id']: item['name'] for item in registry}
    except Exception as e:
        errors.append(f"Failed to read registry: {e}")
        registry_names = {}

    # A. Validate org_chart_export.json
    try:
        with open(org_chart_file, 'r', encoding='utf-8') as f:
            org_chart = json.load(f)
            
        if not isinstance(org_chart, dict):
            errors.append("org_chart_export.json root is not an object.")
        else:
            if org_chart.get("system_name") != "Agent Command Center":
                errors.append("org_chart_export.json system_name is not 'Agent Command Center'.")
            if org_chart.get("version") != "0.1.0":
                errors.append("org_chart_export.json version is not '0.1.0'.")
            if org_chart.get("total_families") != 175:
                errors.append("org_chart_export.json total_families is not 175.")
                
            families = org_chart.get("families", [])
            if not isinstance(families, list) or len(families) != 175:
                errors.append(f"org_chart_export.json families is not a list of exactly 175 (found {len(families) if isinstance(families, list) else type(families)}).")
            else:
                for idx, family in enumerate(families, 1):
                    fid = family.get("id")
                    if type(fid) is not int or fid != idx:
                        errors.append(f"org_chart_export.json family at index {idx-1} does not have sequential ID {idx}.")
                    
                    fname = family.get("name")
                    expected_name = registry_names.get(fid)
                    if fname != expected_name:
                        errors.append(f"org_chart_export.json family {fid} name '{fname}' does not match registry '{expected_name}'.")
                    
                    if family.get("manager") != f"{fid}.M":
                        errors.append(f"org_chart_export.json family {fid} manager is not '{fid}.M'.")
                    if family.get("scribe") != f"{fid}.H":
                        errors.append(f"org_chart_export.json family {fid} scribe is not '{fid}.H'.")
                    if family.get("auditor") != f"{fid}.I":
                        errors.append(f"org_chart_export.json family {fid} auditor is not '{fid}.I'.")
                    
                    folder = family.get("folder", "")
                    if not folder.startswith("02_departments/"):
                        errors.append(f"org_chart_export.json family {fid} folder '{folder}' does not start with '02_departments/'.")
                        
                    family_file = family.get("family_file", "")
                    if not family_file.endswith("/family.json"):
                        errors.append(f"org_chart_export.json family {fid} family_file '{family_file}' does not end with '/family.json'.")
                        
                    readme = family.get("readme", "")
                    if not readme.endswith("/README.md"):
                        errors.append(f"org_chart_export.json family {fid} readme '{readme}' does not end with '/README.md'.")
                        
                    if not isinstance(family.get("departments"), list):
                        errors.append(f"org_chart_export.json family {fid} departments is not a list.")
                        
                    # D. File existence
                    if folder:
                        folder_path = os.path.join(base_dir, folder)
                        if not os.path.isdir(folder_path):
                            errors.append(f"Folder does not exist: {folder_path}")
                    if family_file:
                        file_path = os.path.join(base_dir, family_file)
                        if not os.path.isfile(file_path):
                            errors.append(f"family_file does not exist: {file_path}")
                    if readme:
                        readme_path = os.path.join(base_dir, readme)
                        if not os.path.isfile(readme_path):
                            errors.append(f"readme does not exist: {readme_path}")
                            
    except Exception as e:
        errors.append(f"Failed to read/validate org_chart_export.json: {e}")

    # B. Validate dashboard_seed.json
    try:
        with open(dashboard_file, 'r', encoding='utf-8') as f:
            dashboard = json.load(f)
            
        if not isinstance(dashboard, dict):
            errors.append("dashboard_seed.json root is not an object.")
        else:
            if dashboard.get("title") != "Agent Command Center":
                errors.append("dashboard_seed.json title is not 'Agent Command Center'.")
                
            families = dashboard.get("families", [])
            if not isinstance(families, list) or len(families) != 175:
                errors.append(f"dashboard_seed.json families is not a list of exactly 175 (found {len(families) if isinstance(families, list) else type(families)}).")
            else:
                for idx, family in enumerate(families, 1):
                    fid = family.get("id")
                    if type(fid) is not int or fid != idx:
                        errors.append(f"dashboard_seed.json family at index {idx-1} does not have sequential ID {idx}.")
                    
                    label = family.get("label")
                    expected_name = registry_names.get(fid)
                    if label != expected_name:
                        errors.append(f"dashboard_seed.json family {fid} label '{label}' does not match registry '{expected_name}'.")
                    
                    folder = family.get("folder")
                    # lookup corresponding folder in org_chart
                    try:
                        org_folder = org_chart["families"][idx-1]["folder"]
                        if folder != org_folder:
                            errors.append(f"dashboard_seed.json family {fid} folder '{folder}' does not match org_chart_export '{org_folder}'.")
                    except Exception:
                        pass # handled by org_chart validation
                        
                    if family.get("status") != "shell_created":
                        errors.append(f"dashboard_seed.json family {fid} status is not 'shell_created'.")
                        
    except Exception as e:
        errors.append(f"Failed to read/validate dashboard_seed.json: {e}")

    # C. Validate master_department_list.md
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            
        if not lines or lines[0] != "# Master Department Family List":
            errors.append("master_department_list.md does not start with '# Master Department Family List'.")
            
        list_lines = lines[1:]
        if len(list_lines) != 175:
            errors.append(f"master_department_list.md does not contain exactly 175 numbered department lines (found {len(list_lines)}).")
        else:
            if list_lines[0] != "1. Agent Command":
                errors.append(f"master_department_list.md line 1 is '{list_lines[0]}', expected '1. Agent Command'.")
            if list_lines[-1] != "175. Master Archive / Library of Alexandria":
                errors.append(f"master_department_list.md line 175 is '{list_lines[-1]}', expected '175. Master Archive / Library of Alexandria'.")
                
            for idx, line in enumerate(list_lines, 1):
                expected_name = registry_names.get(idx)
                expected_line = f"{idx}. {expected_name}"
                if line != expected_line:
                    errors.append(f"master_department_list.md line {idx} is '{line}', expected '{expected_line}'.")
                    
    except Exception as e:
        errors.append(f"Failed to read/validate master_department_list.md: {e}")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
        
    print("PASS: Export validation successful.")
    sys.exit(0)

if __name__ == '__main__':
    main()
