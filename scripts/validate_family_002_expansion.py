#!/usr/bin/env python3
import json
import os
import sys

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    family_file = os.path.join(base_dir, '02_departments', '002_planning_and_project_control', 'family.json')
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

    if data.get("id") != 2: errors.append("Family id is not 2.")
    if data.get("name") != "Planning & Project Control": errors.append("Family name is not 'Planning & Project Control'.")
    if data.get("manager") != "2.M" or data.get("scribe") != "2.H" or data.get("auditor") != "2.I":
        errors.append("Manager/Scribe/Auditor fields are incorrect.")
        
    depts = data.get("departments", [])
    if not isinstance(depts, list) or len(depts) != 14:
        errors.append(f"Expected exactly 14 departments, found {len(depts) if isinstance(depts, list) else type(depts)}.")
    
    depts_expected = [
        ("2.1", "Project Management Office", ["Project Intake", "Project Planning", "Project Closure"]),
        ("2.2", "Program Management", ["Program Coordination", "Cross-Project Dependency Review", "Program Health Reporting"]),
        ("2.3", "Portfolio Management", ["Portfolio Inventory", "Portfolio Prioritization", "Portfolio Risk Balancing"]),
        ("2.4", "Task Breakdown", ["Work Decomposition", "Task Sequencing", "Task Acceptance Criteria"]),
        ("2.5", "Sprint Planning", ["Sprint Scope Selection", "Sprint Capacity Review", "Sprint Commitment Summary"]),
        ("2.6", "Timeline Management", ["Deadline Mapping", "Schedule Conflict Detection", "Timeline Adjustment"]),
        ("2.7", "Milestone Tracking", ["Milestone Definition", "Milestone Progress Review", "Milestone Completion Check"]),
        ("2.8", "Dependency Management", ["Dependency Identification", "Dependency Owner Assignment", "Dependency Risk Escalation"]),
        ("2.9", "Resource Allocation", ["Resource Need Assessment", "Workload Balancing", "Resource Constraint Review"]),
        ("2.10", "Scope Control", ["Scope Boundary Definition", "Scope Creep Detection", "Scope Change Approval"]),
        ("2.11", "Change Request Management", ["Change Request Intake", "Change Impact Review", "Change Decision Record"]),
        ("2.12", "Delivery Management", ["Delivery Package Assembly", "Delivery Readiness Review", "Delivery Confirmation"]),
        ("2.13", "Status Reporting", ["Status Collection", "Status Summary Writing", "Status Risk Flagging"]),
        ("2.14", "Project Recovery / Rescue", ["Failure Diagnosis", "Recovery Plan Design", "Rescue Execution Tracking"])
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
        
    print("PASS: Planning & Project Control family expansion valid.")
    sys.exit(0)

if __name__ == '__main__':
    main()