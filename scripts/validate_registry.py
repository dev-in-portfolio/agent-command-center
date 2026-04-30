#!/usr/bin/env python3
import json
import os
import sys

# Note: Python standard library does not include YAML parsing.
# For full YAML validation against 01_registry/department_families.yaml,
# an external library like PyYAML is required later. Do not install it now.
# This script uses a JSON fallback to perform basic structure checks.

def validate_family(family):
    required_keys = {"id", "name", "manager", "scribe", "auditor", "departments"}
    if not isinstance(family, dict):
        return False, "Family must be an object/dict"
    
    missing = required_keys - set(family.keys())
    if missing:
        return False, f"Family missing required keys: {', '.join(missing)}"
        
    if not isinstance(family.get("id"), (int, float)):
        return False, "Family 'id' must be a number"
    if not isinstance(family.get("name"), str):
        return False, "Family 'name' must be a string"
    if not isinstance(family.get("manager"), str):
        return False, "Family 'manager' must be a string"
    if not isinstance(family.get("scribe"), str):
        return False, "Family 'scribe' must be a string"
    if not isinstance(family.get("auditor"), str):
        return False, "Family 'auditor' must be a string"
    if not isinstance(family.get("departments"), list):
        return False, "Family 'departments' must be an array/list"
        
    return True, ""

def main():
    registry_dir = os.path.join(os.path.dirname(__file__), '..', '01_registry')
    yaml_file = os.path.join(registry_dir, 'department_families.yaml')
    json_file = os.path.join(registry_dir, 'department_families.json')
    
    # We are required to do basic checks using JSON fallback if YAML is not parseable with stdlib
    if not os.path.exists(json_file):
        print(f"FAIL: YAML parsing requires PyYAML. Fallback {json_file} not found.")
        print("Please provide 01_registry/department_families.json for validation using standard library.")
        sys.exit(1)
        
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FAIL: Invalid JSON in department_families.json: {e}")
        sys.exit(1)
        
    if not isinstance(data, list):
        print("FAIL: Root of department_families.json should be a list/array of families.")
        sys.exit(1)
        
    all_passed = True
    for idx, item in enumerate(data):
        passed, msg = validate_family(item)
        if not passed:
            print(f"FAIL: Family at index {idx} failed validation - {msg}")
            all_passed = False
            
    if all_passed:
        print("PASS: Basic structure checks passed for department_families.json.")
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
