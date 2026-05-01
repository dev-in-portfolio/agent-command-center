#!/usr/bin/env python3
import json
import os
import sys

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    family_file = os.path.join(base_dir, '02_departments', '003_operations', 'family.json')
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

    if data.get("id") != 3: errors.append("Family id is not 3.")
    if data.get("name") != "Operations": errors.append("Family name is not 'Operations'.")
    if data.get("manager") != "3.M" or data.get("scribe") != "3.H" or data.get("auditor") != "3.I":
        errors.append("Manager/Scribe/Auditor fields are incorrect.")
        
    depts = data.get("departments", [])
    if not isinstance(depts, list) or len(depts) != 10:
        errors.append(f"Expected exactly 14 departments, found {len(depts) if isinstance(depts, list) else type(depts)}.")
    
    depts_expected = [
        ("3.1", "Business Operations", ["Operating Rhythm", "Daily Execution Review", "Operational Bottleneck Detection"]),
        ("3.2", "Field Operations", ["Field Task Planning", "Field Status Collection", "Field Issue Escalation"]),
        ("3.3", "Service Delivery", ["Service Request Intake", "Delivery Workflow Coordination", "Service Completion Verification"]),
        ("3.4", "Workflow Design", ["Workflow Mapping", "Workflow Step Definition", "Workflow Failure Point Review"]),
        ("3.5", "Process Improvement", ["Process Gap Detection", "Improvement Recommendation", "Improvement Implementation Review"]),
        ("3.6", "Scheduling", ["Schedule Creation", "Schedule Conflict Review", "Schedule Update Coordination"]),
        ("3.7", "Logistics", ["Movement Planning", "Route / Transfer Coordination", "Logistics Exception Handling"]),
        ("3.8", "Dispatch", ["Dispatch Queue Review", "Assignment Routing", "Dispatch Confirmation"]),
        ("3.9", "Inventory Control", ["Inventory Count Tracking", "Stock Level Review", "Inventory Exception Reporting"]),
        ("3.10", "Fulfillment", ["Fulfillment Intake", "Fulfillment Assembly", "Fulfillment Completion Check"]),
        ("3.11", "Production Coordination", ["Production Schedule Coordination", "Production Handoff Tracking", "Production Status Review"]),
        ("3.12", "Facilities Operations", ["Facility Readiness Review", "Maintenance Request Routing", "Facility Issue Tracking"]),
        ("3.13", "Vendor Coordination", ["Vendor Request Intake", "Vendor Status Follow-Up", "Vendor Performance Notes"]),
        ("3.14", "Standard Operating Procedures", ["SOP Drafting", "SOP Review", "SOP Update Control"])
    ]

    expected_roles = [
        "Realist", "Overachiever", "Dreamer", "Timid", "Overprotective",
        "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"
    ]
    role_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    
    if isinstance(depts, list):
        for i, dept in enumerate(depts):
            if i >= len(depts_expected): break
            exp_d_id, exp_d_name, exp_u_names = depts_expected[i]
            
            if dept.get("id") != exp_d_id: errors.append(f"Department ID expected {exp_d_id}, found {dept.get('id')}.")
            if dept.get("name") != exp_d_name: errors.append(f"Department name expected {exp_d_name}, found {dept.get('name')}.")
            
            d_id = dept.get("id")
            if dept.get("manager") != f"{d_id}.M": errors.append(f"Manager incorrect for {d_id}")
            if dept.get("scribe") != f"{d_id}.H": errors.append(f"Scribe incorrect for {d_id}")
            if dept.get("auditor") != f"{d_id}.I": errors.append(f"Auditor incorrect for {d_id}")
            
            units = dept.get("units", [])
            if not isinstance(units, list) or len(units) != 3:
                errors.append(f"Expected 3 units in {d_id}, found {len(units) if isinstance(units, list) else type(units)}.")
            
            if isinstance(units, list):
                for j, unit in enumerate(units):
                    if j >= len(exp_u_names): break
                    expected_u_id = f"{d_id}.{j+1}"
                    expected_u_name = exp_u_names[j]
                    
                    if unit.get("id") != expected_u_id:
                        errors.append(f"Unit ID expected {expected_u_id}, found {unit.get('id')}.")
                    if unit.get("name") != expected_u_name:
                        errors.append(f"Unit name expected {expected_u_name}, found {unit.get('name')}.")
                    
                    u_id = unit.get("id")
                    team = unit.get("team", [])
                    if not isinstance(team, list) or len(team) != 9:
                        errors.append(f"Expected exactly 9 team roles in {u_id}, found {len(team) if isinstance(team, list) else type(team)}.")
                    
                    if isinstance(team, list):
                        for k, member in enumerate(team):
                            if k >= len(expected_roles): break
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
        
    print("PASS: Operations family expansion valid.")
    sys.exit(0)

if __name__ == '__main__':
    main()
