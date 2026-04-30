#!/usr/bin/env python3
import json
import os
import sys

EXPECTED_FAMILIES = [
    "Agent Command", "Planning & Project Control", "Operations", "Research & Intelligence", 
    "Data & Knowledge", "Creation & Production", "Engineering & Automation", "Quality, Risk & Compliance", 
    "Business Growth", "Finance & Administration", "Industry Divisions", "Personal Operating System", 
    "HR, Training & Enablement", "Communications & Public Relations", "Manufacturing, Print & Physical Production", 
    "Facilities & Event Operations", "Ethics & Safety", "Strategy, Innovation & R&D", "Community & Ecosystem", 
    "Education & Instructional Systems", "Media & Content Production", "Localization & Accessibility", 
    "Funding, Grants & Capital", "Government, Public Sector & Civic Operations", "Healthcare & Wellness Division", 
    "Real Estate & Property Division", "E-Commerce & Retail Division", "Intellectual Property, Rights & Licensing", 
    "Sustainability & Environmental Operations", "Agent Lab & System Evolution", "Model Operations & AI Infrastructure", 
    "Evaluation & Benchmarking", "Human Review & Approval Operations", "Standards, Templates & Methodology", 
    "Workflow Control Tower", "Regulatory Monitoring & Change Intelligence", "Knowledge Security & Information Classification", 
    "Simulation, Forecasting & Decision Games", "Negotiation & Deal Desk", "Reputation, Trust & Brand Risk", 
    "Customer Insight & Voice of Customer", "Offer Design & Productized Services", "Knowledge Products & Course Production", 
    "Talent Marketplace & Freelance Operations", "Recruiting, Career & Professional Positioning", 
    "Portfolio, Case Studies & Proof Assets", "Personal Productivity & Time Management", "Life Administration", 
    "Personal Knowledge, Learning & Skill Building", "Creative Studio & Story Worlds", "Brand, Identity & Personal Mythology", 
    "Personal AI Companion Architecture", "Prompt Systems & Instruction Architecture", "Memory Engineering & Context Architecture", 
    "Agent Society & Internal Culture", "Autonomous Operations Control", "Multi-Agent Orchestration & Swarm Control", 
    "Tool Operations & External Access", "Interface, Dashboard & Control Panels", "Experimental Systems & Weird Lab", 
    "Archives, Museums & Collection Management", "Scientific Research & Lab Operations", "Investor Research & Market Intelligence", 
    "Relationship Intelligence & Network Management", "Legal Operations & Case Management", "Investigations & Due Diligence", 
    "Personal Finance, Tax & Household Economy", "Travel, Field Work & Mobility Operations", 
    "Home, Workshop & Physical Project Builds", "Humor, Entertainment & Engagement Systems", 
    "Spiritual, Philosophical & Meaning Systems", "Emotional Intelligence & Self-Regulation Systems", 
    "Negotiation, Conflict & Mediation Systems", "Debate, Argument & Critical Thinking Systems", 
    "Creativity, Ideation & Concept Generation", "Decision Memory & Lessons Learned", "Environmental Scanning & Opportunity Radar", 
    "Standards of Evidence & Source Hierarchy", "User Experience Research & Human Factors", 
    "Experimental Governance & Sandbox Control", "Agent Memory Governance & Recall Control", 
    "Version Control, Releases & Change Management", "API Economy, Platform Access & Usage Limits", 
    "Infrastructure Economics & Compute Planning", "Agent Procurement, Hiring & Role Marketplace", 
    "Agent Labor Relations & Internal Governance", "Emotional Brand Experience & Client Perception", 
    "Strategic Memory, Institutional Knowledge & Lore", "Narrative Intelligence & Explanation Design", 
    "Meta-Reasoning & Cognitive Control", "Multi-Modal Intelligence & Artifact Understanding", 
    "Data Visualization & Information Design", "Conversation Design & Dialogue Systems", "Trust, Transparency & Explainability", 
    "Compliance Evidence, Attestation & Regulated Deliverables", "Digital Asset Management & Creative Libraries", 
    "Forms, Intake & Structured Data Collection", "Inbox, Notifications & Signal Management", 
    "Calendar, Scheduling & Time Intelligence", "Master Control, Meta-Architecture & System Constitution", 
    "Cross-Project Intelligence & Pattern Transfer", "Error Recovery, Apology & Repair Systems", 
    "Attention Management & Cognitive Workspace", "User Intent Forensics", "User Preference Engine", 
    "Command Language & Shortcut Systems", "Personal Archive, Vaults & Shelving Systems", "Client-Facing Asset Factory", 
    "Agent-Based Business Process Outsourcing", "System Map, Visualization & Architecture Diagrams", 
    "Knowledge Monetization & Asset Commercialization", "Enterprise Knowledge Base & Internal Wiki", 
    "Scenario Library & Playbook Systems", "Marketplace Intelligence & Commercial Positioning", 
    "Platform Strategy & Distribution Channels", "Business Rules Engine", "Ontology, Taxonomy & Semantic Systems", 
    "Knowledge Graph & Relationship Mapping", "Data Pipelines & ETL Operations", "Search, Discovery & Retrieval Operations", 
    "Data Labeling, Annotation & Training Sets", "Personal Data Rooms & Secure Project Spaces", 
    "Identity, Access & Permission Architecture", "Data Privacy, Consent & Retention Operations", 
    "Integration Testing & End-to-End Validation", "Agent Observability, Telemetry & Run Analytics", 
    "State Management & Workflow Memory", "Work Product Governance & Deliverable Standards", 
    "Knowledge Quality, Currency & Source Freshness", "Agent Economy, Internal Costing & Resource Allocation", 
    "Approval UX, Review Queues & Human Control", "Agent Marketplace, Templates & Reusable Crews", 
    "Agent Conversation Memory & Internal Messaging", "External Action Governance", "Work Intake, Scoping & Triage", 
    "Task Decomposition & Work Package Design", "Department Dependency Graph & Routing Matrix", 
    "Output Assembly, Synthesis & Final Answer Design", "Long-Running Work, Checkpointing & Resumability", 
    "Final Boss Layer: System-of-Systems Governance", "Agent Governance Testing & Constitutional Simulation", 
    "Agent Identity, Role Clarity & Persona Control", "Agent Contracting & Service-Level Agreements", 
    "Agent Tool Safety, Sandboxing & Permission Firewalls", "Agent Ethics Board & Value Alignment Office", 
    "Agent Procurement Stack & Vendor Ecosystem", "Agent Learning Loops & Continuous Improvement", 
    "Multi-Tenant, Multi-Client & Workspace Management", "Agent Reputation, Reliability & Trust Scoring", 
    "Completion Architecture & Definition of Done", "Legal Evidence Exhibit Production", "Compliance Training Academy", 
    "Disaster Simulation Lab", "Public Launch Command Center", "Franchise, Replication & Scaling Systems", 
    "Licensing & White-Label Operations", "Agent App Store & Plugin Ecosystem", "Client Portal Operations", 
    "Knowledge Graph Visualization Studio", "AI Safety Red-Team Lab", "Prompt Injection Defense Office", 
    "Data Backup & Cold Storage", "Digital Legacy Planning", "Reputation Fire Drill Team", "Systems Migration Office", 
    "Mobile App Operations", "Voice, Phone & Conversational Agent Operations", "Physical Mail & Print Outreach", 
    "CRM Operations", "Lead Nurture Factory", "Revenue Operations", "Customer Education Academy", 
    "Workflow Certification Office", "Agent Incident Court", "Master Archive / Library of Alexandria"
]

def main():
    registry_dir = os.path.join(os.path.dirname(__file__), '..', '01_registry')
    json_file = os.path.join(registry_dir, 'department_families.json')
    sample_file = os.path.join(os.path.dirname(__file__), '..', '02_departments', '001_agent_command', 'family.json')
    
    errors = []

    if not os.path.exists(json_file):
        errors.append(f"Fallback {json_file} not found.")
    else:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not isinstance(data, list):
                errors.append("Root of department_families.json must be a list.")
            else:
                if len(data) != 175:
                    errors.append(f"List must contain exactly 175 department families, found {len(data)}.")
                
                ids = []
                names = []
                
                for idx, family in enumerate(data):
                    if not isinstance(family, dict):
                        errors.append(f"Family at index {idx} is not an object/dict.")
                        continue
                        
                    fid = family.get("id")
                    if type(fid) is not int:
                        errors.append(f"Family at index {idx} id must be an integer, not float or other.")
                    else:
                        ids.append(fid)
                    
                    fname = family.get("name")
                    names.append(fname)
                    
                    if fid is not None:
                        manager = family.get("manager")
                        if manager != f"{fid}.M":
                            errors.append(f"Family {fid} manager '{manager}' does not equal '{fid}.M'.")
                        
                        scribe = family.get("scribe")
                        if scribe != f"{fid}.H":
                            errors.append(f"Family {fid} scribe '{scribe}' does not equal '{fid}.H'.")
                            
                        auditor = family.get("auditor")
                        if auditor != f"{fid}.I":
                            errors.append(f"Family {fid} auditor '{auditor}' does not equal '{fid}.I'.")
                            
                    if not isinstance(family.get("departments"), list):
                        errors.append(f"Family {fid} 'departments' must be a list.")
                
                # Check IDs are sequential 1 through 175 with no gaps
                expected_ids = list(range(1, 176))
                if ids != expected_ids:
                    errors.append("IDs are not sequential from 1 through 175 with no gaps.")
                
                # Duplicate checks
                if len(ids) != len(set(ids)):
                    errors.append("Duplicate IDs found.")
                if len(names) != len(set(names)):
                    errors.append("Duplicate names found.")
                    
                # Validate exact expected names
                for exp_id, exp_name in enumerate(EXPECTED_FAMILIES, 1):
                    found = False
                    for f in data:
                        if f.get("id") == exp_id:
                            found = True
                            if f.get("name") != exp_name:
                                errors.append(f"Family {exp_id} name '{f.get('name')}' does not match expected '{exp_name}'.")
                            break
                    if not found:
                        errors.append(f"Family {exp_id} expected but not found in data.")

        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in department_families.json: {e}")

    # Validate sample file
    if not os.path.exists(sample_file):
        errors.append(f"Sample file {sample_file} not found.")
    else:
        try:
            with open(sample_file, 'r', encoding='utf-8') as f:
                sample_data = json.load(f)
                
            if sample_data.get("id") != 1:
                errors.append("Sample file id is not 1.")
            if sample_data.get("name") != "Agent Command":
                errors.append("Sample file name is not 'Agent Command'.")
            if sample_data.get("manager") != "1.M" or sample_data.get("scribe") != "1.H" or sample_data.get("auditor") != "1.I":
                errors.append("Sample file manager/scribe/auditor are not 1.M / 1.H / 1.I.")
                
            depts = sample_data.get("departments", [])
            dept_found = False
            unit_found = False
            team_correct = False
            expected_team_ids = [
                "1.1.1.1A", "1.1.1.1B", "1.1.1.1C", "1.1.1.1D", "1.1.1.1E",
                "1.1.1.1F", "1.1.1.1G", "1.1.1.1H", "1.1.1.1I"
            ]
            
            for dept in depts:
                if dept.get("id") == "1.1" and dept.get("name") == "Executive Command":
                    dept_found = True
                    units = dept.get("units", [])
                    for unit in units:
                        if unit.get("id") == "1.1.1" and unit.get("name") == "Mission Direction":
                            unit_found = True
                            team = unit.get("team", [])
                            team_ids = [member.get("id") for member in team]
                            if team_ids == expected_team_ids:
                                team_correct = True
                            else:
                                errors.append(f"Sample unit team ids {team_ids} do not match expected {expected_team_ids}.")
            
            if not dept_found:
                errors.append("Sample file does not contain department 1.1 Executive Command.")
            if not unit_found:
                errors.append("Sample file does not contain unit 1.1.1 Mission Direction.")
            if unit_found and not team_correct:
                pass # Error added above
                
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in sample file {sample_file}: {e}")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    else:
        print("PASS: Registry validation successful.")
        sys.exit(0)

if __name__ == '__main__':
    main()
