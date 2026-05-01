import json
import os
import sys
import re

EXPECTED = {
    "165": {
        "name": "Systems Migration Office",
        "departments": {
            "165.1": {
                "name": "Migration Intake",
                "units": {
                    "165.1.1": "Migration Request Capture",
                    "165.1.2": "Source System Review",
                    "165.1.3": "Migration Intake Summary"
                }
            },
            "165.2": {
                "name": "Migration Scope Mapping",
                "units": {
                    "165.2.1": "System Boundary Definition",
                    "165.2.2": "Data And Workflow Inventory",
                    "165.2.3": "Scope Map Update"
                }
            },
            "165.3": {
                "name": "Source System Assessment",
                "units": {
                    "165.3.1": "Legacy System Inventory",
                    "165.3.2": "Dependency Risk Review",
                    "165.3.3": "Source Readiness Notes"
                }
            },
            "165.4": {
                "name": "Target System Design",
                "units": {
                    "165.4.1": "Target Requirement Capture",
                    "165.4.2": "Future State Mapping",
                    "165.4.3": "Target Design Summary"
                }
            },
            "165.5": {
                "name": "Migration Plan Development",
                "units": {
                    "165.5.1": "Migration Step Sequencing",
                    "165.5.2": "Cutover Strategy Draft",
                    "165.5.3": "Migration Plan QA"
                }
            },
            "165.6": {
                "name": "Data Migration Operations",
                "units": {
                    "165.6.1": "Data Extract Review",
                    "165.6.2": "Transformation Mapping",
                    "165.6.3": "Load Verification Notes"
                }
            },
            "165.7": {
                "name": "Migration Testing",
                "units": {
                    "165.7.1": "Test Case Selection",
                    "165.7.2": "Migration Result Review",
                    "165.7.3": "Migration Test Summary"
                }
            },
            "165.8": {
                "name": "Cutover Management",
                "units": {
                    "165.8.1": "Cutover Window Planning",
                    "165.8.2": "Go-Live Checklist Review",
                    "165.8.3": "Cutover Decision Record"
                }
            },
            "165.9": {
                "name": "Migration Risk Governance",
                "units": {
                    "165.9.1": "Migration Risk Detection",
                    "165.9.2": "Rollback Path Review",
                    "165.9.3": "Risk Governance Notes"
                }
            },
            "165.10": {
                "name": "Migration Dashboard",
                "units": {
                    "165.10.1": "Migration Signal Collection",
                    "165.10.2": "Cutover Status Summary",
                    "165.10.3": "Dashboard Update"
                }
            }
        }
    },
    "166": {
        "name": "Mobile App Operations",
        "departments": {
            "166.1": {
                "name": "Mobile App Intake",
                "units": {
                    "166.1.1": "App Request Capture",
                    "166.1.2": "Platform Requirement Review",
                    "166.1.3": "Mobile Intake Summary"
                }
            },
            "166.2": {
                "name": "Mobile Feature Planning",
                "units": {
                    "166.2.1": "Feature Candidate Capture",
                    "166.2.2": "User Flow Review",
                    "166.2.3": "Feature Plan Update"
                }
            },
            "166.3": {
                "name": "Mobile UX Review",
                "units": {
                    "166.3.1": "Screen Flow Capture",
                    "166.3.2": "Touch Interaction Review",
                    "166.3.3": "Mobile UX Notes"
                }
            },
            "166.4": {
                "name": "App Build Coordination",
                "units": {
                    "166.4.1": "Build Requirement Mapping",
                    "166.4.2": "Release Branch Review",
                    "166.4.3": "Build Coordination Notes"
                }
            },
            "166.5": {
                "name": "Device Compatibility Testing",
                "units": {
                    "166.5.1": "Device Matrix Definition",
                    "166.5.2": "Compatibility Test Review",
                    "166.5.3": "Compatibility Findings"
                }
            },
            "166.6": {
                "name": "App Store Submission",
                "units": {
                    "166.6.1": "Store Requirement Capture",
                    "166.6.2": "Listing Asset Review",
                    "166.6.3": "Submission Status Update"
                }
            },
            "166.7": {
                "name": "Mobile Analytics Review",
                "units": {
                    "166.7.1": "Mobile Metric Collection",
                    "166.7.2": "User Behavior Review",
                    "166.7.3": "Analytics Recommendation"
                }
            },
            "166.8": {
                "name": "Crash And Bug Monitoring",
                "units": {
                    "166.8.1": "Crash Signal Capture",
                    "166.8.2": "Bug Severity Review",
                    "166.8.3": "Fix Priority Notes"
                }
            },
            "166.9": {
                "name": "Mobile Governance",
                "units": {
                    "166.9.1": "Mobile Rule Definition",
                    "166.9.2": "Platform Exception Review",
                    "166.9.3": "Governance Record Update"
                }
            },
            "166.10": {
                "name": "Mobile Dashboard",
                "units": {
                    "166.10.1": "Mobile Signal Collection",
                    "166.10.2": "App Status Summary",
                    "166.10.3": "Dashboard Update"
                }
            }
        }
    },
    "167": {
        "name": "Voice, Phone & Conversational Agent Operations",
        "departments": {
            "167.1": {
                "name": "Voice Channel Intake",
                "units": {
                    "167.1.1": "Voice Use Case Capture",
                    "167.1.2": "Call Flow Requirement Review",
                    "167.1.3": "Voice Intake Summary"
                }
            },
            "167.2": {
                "name": "Call Flow Design",
                "units": {
                    "167.2.1": "Caller Journey Mapping",
                    "167.2.2": "Branch Logic Draft",
                    "167.2.3": "Call Flow QA"
                }
            },
            "167.3": {
                "name": "Conversational Agent Script",
                "units": {
                    "167.3.1": "Script Objective Capture",
                    "167.3.2": "Dialogue Turn Draft",
                    "167.3.3": "Script Clarity Review"
                }
            },
            "167.4": {
                "name": "Voice Experience Testing",
                "units": {
                    "167.4.1": "Voice Test Scenario Selection",
                    "167.4.2": "Audio Interaction Review",
                    "167.4.3": "Voice Test Findings"
                }
            },
            "167.5": {
                "name": "Phone Routing Operations",
                "units": {
                    "167.5.1": "Routing Rule Definition",
                    "167.5.2": "Escalation Path Review",
                    "167.5.3": "Routing Update Notes"
                }
            },
            "167.6": {
                "name": "Call Recording Review",
                "units": {
                    "167.6.1": "Recording Signal Capture",
                    "167.6.2": "Quality Pattern Review",
                    "167.6.3": "Recording Review Notes"
                }
            },
            "167.7": {
                "name": "Voice Compliance Review",
                "units": {
                    "167.7.1": "Disclosure Requirement Capture",
                    "167.7.2": "Consent Boundary Review",
                    "167.7.3": "Voice Compliance Notes"
                }
            },
            "167.8": {
                "name": "Live Agent Handoff",
                "units": {
                    "167.8.1": "Handoff Trigger Definition",
                    "167.8.2": "Context Transfer Review",
                    "167.8.3": "Handoff Confirmation Notes"
                }
            },
            "167.9": {
                "name": "Voice Governance",
                "units": {
                    "167.9.1": "Voice Rule Definition",
                    "167.9.2": "Call Exception Review",
                    "167.9.3": "Governance Record Update"
                }
            },
            "167.10": {
                "name": "Voice Dashboard",
                "units": {
                    "167.10.1": "Voice Signal Collection",
                    "167.10.2": "Conversation Status Summary",
                    "167.10.3": "Dashboard Update"
                }
            }
        }
    },
    "168": {
        "name": "Physical Mail & Print Outreach",
        "departments": {
            "168.1": {
                "name": "Mail Campaign Intake",
                "units": {
                    "168.1.1": "Campaign Objective Capture",
                    "168.1.2": "Audience List Review",
                    "168.1.3": "Mail Intake Summary"
                }
            },
            "168.2": {
                "name": "Print Piece Design",
                "units": {
                    "168.2.1": "Format Requirement Capture",
                    "168.2.2": "Copy And Layout Draft",
                    "168.2.3": "Print Piece QA"
                }
            },
            "168.3": {
                "name": "Mailing List Preparation",
                "units": {
                    "168.3.1": "Address List Capture",
                    "168.3.2": "List Hygiene Review",
                    "168.3.3": "Mailing List Update"
                }
            },
            "168.4": {
                "name": "Print Vendor Coordination",
                "units": {
                    "168.4.1": "Vendor Requirement Review",
                    "168.4.2": "Print Quote Capture",
                    "168.4.3": "Vendor Coordination Notes"
                }
            },
            "168.5": {
                "name": "Postal Compliance Review",
                "units": {
                    "168.5.1": "Postal Rule Capture",
                    "168.5.2": "Mail Class Review",
                    "168.5.3": "Postal Compliance Notes"
                }
            },
            "168.6": {
                "name": "Mail Drop Scheduling",
                "units": {
                    "168.6.1": "Drop Date Planning",
                    "168.6.2": "Delivery Window Review",
                    "168.6.3": "Schedule Confirmation Notes"
                }
            },
            "168.7": {
                "name": "Response Tracking",
                "units": {
                    "168.7.1": "Response Signal Capture",
                    "168.7.2": "Campaign Attribution Review",
                    "168.7.3": "Response Tracking Update"
                }
            },
            "168.8": {
                "name": "Print Quality Control",
                "units": {
                    "168.8.1": "Proof Review",
                    "168.8.2": "Defect Detection",
                    "168.8.3": "Print Approval Notes"
                }
            },
            "168.9": {
                "name": "Mail Governance",
                "units": {
                    "168.9.1": "Outreach Rule Definition",
                    "168.9.2": "Suppression Exception Review",
                    "168.9.3": "Governance Record Update"
                }
            },
            "168.10": {
                "name": "Mail Dashboard",
                "units": {
                    "168.10.1": "Mail Signal Collection",
                    "168.10.2": "Outreach Status Summary",
                    "168.10.3": "Dashboard Update"
                }
            }
        }
    },
    "169": {
        "name": "CRM Operations",
        "departments": {
            "169.1": {
                "name": "CRM Intake",
                "units": {
                    "169.1.1": "CRM Request Capture",
                    "169.1.2": "Object Requirement Review",
                    "169.1.3": "CRM Intake Summary"
                }
            },
            "169.2": {
                "name": "Contact Record Management",
                "units": {
                    "169.2.1": "Contact Data Capture",
                    "169.2.2": "Duplicate Review",
                    "169.2.3": "Contact Record Update"
                }
            },
            "169.3": {
                "name": "Pipeline Configuration",
                "units": {
                    "169.3.1": "Pipeline Stage Definition",
                    "169.3.2": "Deal Flow Mapping",
                    "169.3.3": "Pipeline Setup Notes"
                }
            },
            "169.4": {
                "name": "CRM Field Management",
                "units": {
                    "169.4.1": "Field Requirement Capture",
                    "169.4.2": "Field Type Review",
                    "169.4.3": "Field Configuration Update"
                }
            },
            "169.5": {
                "name": "CRM Automation Rules",
                "units": {
                    "169.5.1": "Automation Trigger Capture",
                    "169.5.2": "Workflow Action Review",
                    "169.5.3": "Automation Rule Update"
                }
            },
            "169.6": {
                "name": "CRM Data Hygiene",
                "units": {
                    "169.6.1": "Dirty Data Detection",
                    "169.6.2": "Correction Rule Review",
                    "169.6.3": "Hygiene Action Notes"
                }
            },
            "169.7": {
                "name": "CRM Reporting",
                "units": {
                    "169.7.1": "Report Requirement Capture",
                    "169.7.2": "Metric Definition Review",
                    "169.7.3": "CRM Report Update"
                }
            },
            "169.8": {
                "name": "CRM Integration Review",
                "units": {
                    "169.8.1": "Integration Candidate Capture",
                    "169.8.2": "Sync Requirement Review",
                    "169.8.3": "Integration Notes"
                }
            },
            "169.9": {
                "name": "CRM Governance",
                "units": {
                    "169.9.1": "CRM Rule Definition",
                    "169.9.2": "Access Exception Review",
                    "169.9.3": "Governance Record Update"
                }
            },
            "169.10": {
                "name": "CRM Dashboard",
                "units": {
                    "169.10.1": "CRM Signal Collection",
                    "169.10.2": "Pipeline Status Summary",
                    "169.10.3": "Dashboard Update"
                }
            }
        }
    },
    "170": {
        "name": "Lead Nurture Factory",
        "departments": {
            "170.1": {
                "name": "Lead Nurture Intake",
                "units": {
                    "170.1.1": "Lead Source Capture",
                    "170.1.2": "Nurture Goal Review",
                    "170.1.3": "Lead Intake Summary"
                }
            },
            "170.2": {
                "name": "Segment Design",
                "units": {
                    "170.2.1": "Segment Criteria Definition",
                    "170.2.2": "Audience Fit Review",
                    "170.2.3": "Segment Map Update"
                }
            },
            "170.3": {
                "name": "Nurture Sequence Design",
                "units": {
                    "170.3.1": "Sequence Objective Capture",
                    "170.3.2": "Message Step Mapping",
                    "170.3.3": "Sequence QA"
                }
            },
            "170.4": {
                "name": "Follow-Up Copy Production",
                "units": {
                    "170.4.1": "Message Purpose Capture",
                    "170.4.2": "Follow-Up Copy Draft",
                    "170.4.3": "Copy Quality Review"
                }
            },
            "170.5": {
                "name": "Lead Scoring",
                "units": {
                    "170.5.1": "Scoring Factor Definition",
                    "170.5.2": "Behavior Signal Review",
                    "170.5.3": "Lead Score Update"
                }
            },
            "170.6": {
                "name": "Nurture Automation Setup",
                "units": {
                    "170.6.1": "Automation Trigger Definition",
                    "170.6.2": "Delay Rule Review",
                    "170.6.3": "Automation Setup Notes"
                }
            },
            "170.7": {
                "name": "Engagement Monitoring",
                "units": {
                    "170.7.1": "Engagement Signal Collection",
                    "170.7.2": "Response Pattern Review",
                    "170.7.3": "Engagement Summary"
                }
            },
            "170.8": {
                "name": "Re-Engagement Campaigns",
                "units": {
                    "170.8.1": "Dormant Lead Detection",
                    "170.8.2": "Re-Engagement Offer Review",
                    "170.8.3": "Campaign Recommendation"
                }
            },
            "170.9": {
                "name": "Nurture Governance",
                "units": {
                    "170.9.1": "Nurture Rule Definition",
                    "170.9.2": "Contact Frequency Review",
                    "170.9.3": "Governance Record Update"
                }
            },
            "170.10": {
                "name": "Nurture Dashboard",
                "units": {
                    "170.10.1": "Lead Signal Collection",
                    "170.10.2": "Nurture Status Summary",
                    "170.10.3": "Dashboard Update"
                }
            }
        }
    },
    "171": {
        "name": "Revenue Operations",
        "departments": {
            "171.1": {
                "name": "Revenue Operations Intake",
                "units": {
                    "171.1.1": "Revenue Request Capture",
                    "171.1.2": "Revenue Process Review",
                    "171.1.3": "RevOps Intake Summary"
                }
            },
            "171.2": {
                "name": "Funnel Metrics",
                "units": {
                    "171.2.1": "Funnel Stage Definition",
                    "171.2.2": "Conversion Metric Review",
                    "171.2.3": "Funnel Metric Update"
                }
            },
            "171.3": {
                "name": "Sales Process Alignment",
                "units": {
                    "171.3.1": "Sales Step Capture",
                    "171.3.2": "Handoff Alignment Review",
                    "171.3.3": "Process Alignment Notes"
                }
            },
            "171.4": {
                "name": "Revenue Forecasting",
                "units": {
                    "171.4.1": "Forecast Input Capture",
                    "171.4.2": "Probability Review",
                    "171.4.3": "Forecast Summary"
                }
            },
            "171.5": {
                "name": "Pricing Operations",
                "units": {
                    "171.5.1": "Pricing Rule Capture",
                    "171.5.2": "Discount Boundary Review",
                    "171.5.3": "Pricing Operations Notes"
                }
            },
            "171.6": {
                "name": "Revenue Reporting",
                "units": {
                    "171.6.1": "Revenue Data Collection",
                    "171.6.2": "Report Accuracy Review",
                    "171.6.3": "Revenue Report Update"
                }
            },
            "171.7": {
                "name": "Sales Enablement Operations",
                "units": {
                    "171.7.1": "Enablement Need Capture",
                    "171.7.2": "Asset Fit Review",
                    "171.7.3": "Enablement Notes"
                }
            },
            "171.8": {
                "name": "Revenue Leakage Review",
                "units": {
                    "171.8.1": "Leakage Signal Detection",
                    "171.8.2": "Process Gap Review",
                    "171.8.3": "Leakage Reduction Notes"
                }
            },
            "171.9": {
                "name": "RevOps Governance",
                "units": {
                    "171.9.1": "Revenue Rule Definition",
                    "171.9.2": "Exception Review",
                    "171.9.3": "Governance Record Update"
                }
            },
            "171.10": {
                "name": "Revenue Dashboard",
                "units": {
                    "171.10.1": "Revenue Signal Collection",
                    "171.10.2": "Forecast Status Summary",
                    "171.10.3": "Dashboard Update"
                }
            }
        }
    },
    "172": {
        "name": "Customer Education Academy",
        "departments": {
            "172.1": {
                "name": "Education Program Intake",
                "units": {
                    "172.1.1": "Learning Need Capture",
                    "172.1.2": "Customer Audience Review",
                    "172.1.3": "Education Intake Summary"
                }
            },
            "172.2": {
                "name": "Curriculum Path Design",
                "units": {
                    "172.2.1": "Learning Path Definition",
                    "172.2.2": "Module Sequence Review",
                    "172.2.3": "Curriculum Path Update"
                }
            },
            "172.3": {
                "name": "Customer Lesson Production",
                "units": {
                    "172.3.1": "Lesson Objective Capture",
                    "172.3.2": "Lesson Content Draft",
                    "172.3.3": "Lesson QA"
                }
            },
            "172.4": {
                "name": "Tutorial Asset Creation",
                "units": {
                    "172.4.1": "Tutorial Topic Selection",
                    "172.4.2": "Step Instruction Draft",
                    "172.4.3": "Tutorial Asset Review"
                }
            },
            "172.5": {
                "name": "Knowledge Check Design",
                "units": {
                    "172.5.1": "Checkpoint Criteria Capture",
                    "172.5.2": "Question Draft Review",
                    "172.5.3": "Knowledge Check Update"
                }
            },
            "172.6": {
                "name": "Education Delivery Operations",
                "units": {
                    "172.6.1": "Delivery Channel Selection",
                    "172.6.2": "Schedule And Access Review",
                    "172.6.3": "Delivery Plan Notes"
                }
            },
            "172.7": {
                "name": "Learner Progress Tracking",
                "units": {
                    "172.7.1": "Progress Signal Capture",
                    "172.7.2": "Completion Review",
                    "172.7.3": "Progress Record Update"
                }
            },
            "172.8": {
                "name": "Education Feedback Loop",
                "units": {
                    "172.8.1": "Feedback Signal Collection",
                    "172.8.2": "Learning Gap Review",
                    "172.8.3": "Feedback Action Notes"
                }
            },
            "172.9": {
                "name": "Education Governance",
                "units": {
                    "172.9.1": "Education Rule Definition",
                    "172.9.2": "Curriculum Exception Review",
                    "172.9.3": "Governance Record Update"
                }
            },
            "172.10": {
                "name": "Education Dashboard",
                "units": {
                    "172.10.1": "Education Signal Collection",
                    "172.10.2": "Learner Status Summary",
                    "172.10.3": "Dashboard Update"
                }
            }
        }
    },
    "173": {
        "name": "Workflow Certification Office",
        "departments": {
            "173.1": {
                "name": "Certification Intake",
                "units": {
                    "173.1.1": "Certification Request Capture",
                    "173.1.2": "Workflow Candidate Review",
                    "173.1.3": "Certification Intake Summary"
                }
            },
            "173.2": {
                "name": "Certification Standard Design",
                "units": {
                    "173.2.1": "Standard Criteria Definition",
                    "173.2.2": "Evidence Requirement Mapping",
                    "173.2.3": "Standard Design Notes"
                }
            },
            "173.3": {
                "name": "Workflow Assessment",
                "units": {
                    "173.3.1": "Workflow Evidence Collection",
                    "173.3.2": "Standard Fit Review",
                    "173.3.3": "Assessment Finding Summary"
                }
            },
            "173.4": {
                "name": "Certification Testing",
                "units": {
                    "173.4.1": "Test Case Selection",
                    "173.4.2": "Workflow Test Review",
                    "173.4.3": "Certification Test Summary"
                }
            },
            "173.5": {
                "name": "Certification Decisioning",
                "units": {
                    "173.5.1": "Decision Criteria Review",
                    "173.5.2": "Certification Status Selection",
                    "173.5.3": "Decision Record Update"
                }
            },
            "173.6": {
                "name": "Renewal Review",
                "units": {
                    "173.6.1": "Renewal Trigger Detection",
                    "173.6.2": "Continued Fit Review",
                    "173.6.3": "Renewal Recommendation"
                }
            },
            "173.7": {
                "name": "Certification Registry",
                "units": {
                    "173.7.1": "Certified Workflow Capture",
                    "173.7.2": "Registry Metadata Review",
                    "173.7.3": "Registry Update"
                }
            },
            "173.8": {
                "name": "Nonconformance Handling",
                "units": {
                    "173.8.1": "Nonconformance Detection",
                    "173.8.2": "Correction Path Review",
                    "173.8.3": "Nonconformance Record"
                }
            },
            "173.9": {
                "name": "Certification Governance",
                "units": {
                    "173.9.1": "Certification Rule Definition",
                    "173.9.2": "Exception Review",
                    "173.9.3": "Governance Record Update"
                }
            },
            "173.10": {
                "name": "Certification Dashboard",
                "units": {
                    "173.10.1": "Certification Signal Collection",
                    "173.10.2": "Workflow Status Summary",
                    "173.10.3": "Dashboard Update"
                }
            }
        }
    },
    "174": {
        "name": "Agent Incident Court",
        "departments": {
            "174.1": {
                "name": "Incident Case Intake",
                "units": {
                    "174.1.1": "Incident Claim Capture",
                    "174.1.2": "Case Scope Review",
                    "174.1.3": "Incident Case Summary"
                }
            },
            "174.2": {
                "name": "Evidence Docket",
                "units": {
                    "174.2.1": "Evidence Item Filing",
                    "174.2.2": "Docket Sequence Review",
                    "174.2.3": "Evidence Docket Update"
                }
            },
            "174.3": {
                "name": "Agent Testimony Review",
                "units": {
                    "174.3.1": "Agent Statement Capture",
                    "174.3.2": "Testimony Consistency Review",
                    "174.3.3": "Testimony Finding Notes"
                }
            },
            "174.4": {
                "name": "Incident Argument Mapping",
                "units": {
                    "174.4.1": "Claim Argument Capture",
                    "174.4.2": "Counterargument Review",
                    "174.4.3": "Argument Map Update"
                }
            },
            "174.5": {
                "name": "Responsibility Assessment",
                "units": {
                    "174.5.1": "Responsibility Candidate Review",
                    "174.5.2": "Causal Path Analysis",
                    "174.5.3": "Responsibility Finding"
                }
            },
            "174.6": {
                "name": "Remediation Order Drafting",
                "units": {
                    "174.6.1": "Remedy Requirement Capture",
                    "174.6.2": "Corrective Action Draft",
                    "174.6.3": "Remediation Order Notes"
                }
            },
            "174.7": {
                "name": "Appeals Review",
                "units": {
                    "174.7.1": "Appeal Request Capture",
                    "174.7.2": "Appeal Evidence Review",
                    "174.7.3": "Appeal Decision Notes"
                }
            },
            "174.8": {
                "name": "Precedent Management",
                "units": {
                    "174.8.1": "Precedent Case Capture",
                    "174.8.2": "Similarity Review",
                    "174.8.3": "Precedent Record Update"
                }
            },
            "174.9": {
                "name": "Incident Court Governance",
                "units": {
                    "174.9.1": "Court Rule Definition",
                    "174.9.2": "Exception Review",
                    "174.9.3": "Governance Record Update"
                }
            },
            "174.10": {
                "name": "Incident Court Dashboard",
                "units": {
                    "174.10.1": "Incident Signal Collection",
                    "174.10.2": "Case Status Summary",
                    "174.10.3": "Dashboard Update"
                }
            }
        }
    }
}

FOLDER_MAPPING = {
    "165": "165_systems_migration_office",
    "166": "166_mobile_app_operations",
    "167": "167_voice_phone_and_conversational_agent_operations",
    "168": "168_physical_mail_and_print_outreach",
    "169": "169_crm_operations",
    "170": "170_lead_nurture_factory",
    "171": "171_revenue_operations",
    "172": "172_customer_education_academy",
    "173": "173_workflow_certification_office",
    "174": "174_agent_incident_court"
}

def validate():
    spec_path = "04_workflow_templates/family_expansion_batch_165_174.json"
    with open(spec_path, 'r') as f:
        batch_spec = json.load(f)

    errors = []
    
    # Fidelity strings (checking existence in spec)
    required_strings = [
        "Systems Migration Office",
        "Migration Plan Development",
        "Cutover Management",
        "Mobile App Operations",
        "Device Compatibility Testing",
        "Crash And Bug Monitoring",
        "Voice, Phone & Conversational Agent Operations",
        "Conversational Agent Script",
        "Live Agent Handoff",
        "Physical Mail & Print Outreach",
        "Postal Compliance Review",
        "Print Quality Control",
        "CRM Operations",
        "CRM Automation Rules",
        "CRM Data Hygiene",
        "Lead Nurture Factory",
        "Nurture Sequence Design",
        "Re-Engagement Campaigns",
        "Revenue Operations",
        "Revenue Forecasting",
        "Revenue Leakage Review",
        "Customer Education Academy",
        "Tutorial Asset Creation",
        "Education Feedback Loop",
        "Workflow Certification Office",
        "Certification Decisioning",
        "Nonconformance Handling",
        "Agent Incident Court",
        "Responsibility Assessment",
        "Precedent Management"
    ]
    spec_text = json.dumps(batch_spec)
    for s in required_strings:
        if s not in spec_text:
            errors.append(f"Prompt fidelity string missing from spec: '{s}'")

    # Validate Batch Spec against EXPECTED
    if len(batch_spec) != 10:
        errors.append(f"Batch spec length mismatch: expected 10, found {len(batch_spec)}")
        
    for family in batch_spec:
        fid = family["id"]
        if fid not in EXPECTED:
            errors.append(f"Family {fid} not in EXPECTED")
            continue
        if family["name"] != EXPECTED[fid]["name"]:
            errors.append(f"Family {fid} name mismatch: expected '{EXPECTED[fid]['name']}', found '{family['name']}'")
        
        depts = {d["id"]: d for d in family["departments"]}
        if len(depts) != 10:
            errors.append(f"Family {fid} department count mismatch: expected 10, found {len(depts)}")
            
        for did, dexpect in EXPECTED[fid]["departments"].items():
            if did not in depts:
                errors.append(f"Department {did} missing from batch spec")
                continue
            if depts[did]["name"] != dexpect["name"]:
                errors.append(f"Department {did} name mismatch: expected '{dexpect['name']}', found '{depts[did]['name']}'")
            
            units = {u["id"]: u for u in depts[did]["units"]}
            if len(units) != 3:
                errors.append(f"Department {did} unit count mismatch: expected 3, found {len(units)}")
            for uid, uname in dexpect["units"].items():
                if uid not in units:
                    errors.append(f"Unit {uid} missing from batch spec")
                elif units[uid]["name"] != uname:
                    errors.append(f"Unit {uid} name mismatch in spec: expected '{uname}', found '{units[uid]['name']}'")

    # Validate Files
    for fid, fexpect in EXPECTED.items():
        fname_slug = FOLDER_MAPPING[fid]
        fdir = f"02_departments/{fname_slug}"
        fjson_path = os.path.join(fdir, "family.json")
        readme_path = os.path.join(fdir, "README.md")
        
        if not os.path.exists(fjson_path):
            errors.append(f"File missing: {fjson_path}")
            continue
            
        with open(fjson_path, 'r') as f:
            fjson = json.load(f)
            
        if not isinstance(fjson["id"], int):
            errors.append(f"Family {fid} ID is not an integer in family.json")
        if str(fjson["id"]) != fid:
            errors.append(f"Family ID mismatch in {fjson_path}: expected {fid}, found {fjson['id']}")
        if fjson["name"] != fexpect["name"]:
            errors.append(f"Family name mismatch in {fjson_path}")
            
        if fjson.get("manager") != f"{fid}.M": errors.append(f"Family {fid} manager mismatch")
        if fjson.get("scribe") != f"{fid}.H": errors.append(f"Family {fid} scribe mismatch")
        if fjson.get("auditor") != f"{fid}.I": errors.append(f"Family {fid} auditor mismatch")

        depts = {d["id"]: d for d in fjson["departments"]}
        for did, dexpect in fexpect["departments"].items():
            if did not in depts:
                errors.append(f"Department {did} missing from {fjson_path}")
                continue
            dept = depts[did]
            if dept["name"] != dexpect["name"]:
                errors.append(f"Department {did} name mismatch in {fjson_path}")
            
            if dept.get("manager") != f"{did}.M": errors.append(f"Dept {did} manager mismatch")
            if dept.get("scribe") != f"{did}.H": errors.append(f"Dept {did} scribe mismatch")
            if dept.get("auditor") != f"{did}.I": errors.append(f"Dept {did} auditor mismatch")

            for u in dept["units"]:
                uid = u["id"]
                if uid not in dexpect["units"]:
                    errors.append(f"Unit {uid} not expected in dept {did}")
                    continue
                
                uname = dexpect["units"][uid]
                if u["name"] != uname:
                    errors.append(f"Unit {uid} name mismatch in {fjson_path}: expected '{uname}', found '{u['name']}'")
                
                if len(u["team"]) != 9:
                    errors.append(f"Unit {uid} team size mismatch: expected 9, found {len(u['team'])}")
                for i, role in enumerate(["Realist", "Overachiever", "Dreamer", "Timid", "Overprotective", "Wildcard Intern", "Team Lead / Manager", "Scribe / Shower of Work", "Auditor / Revision Director"]):
                    suffix = ["1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H", "1I"][i]
                    tm = u["team"][i]
                    if not isinstance(tm, dict):
                        errors.append(f"Unit {uid} team member {suffix} is not a dict")
                        continue
                    if tm.get("id") != f"{uid}.{suffix}":
                        errors.append(f"Team member ID mismatch for {uid} {suffix}")
                    if tm.get("role") != role:
                        errors.append(f"Team member role mismatch for {uid} {suffix}")

        if not os.path.exists(readme_path):
            errors.append(f"File missing: {readme_path}")
            continue
            
        with open(readme_path, 'r') as f:
            readme = f.read()
            
        if f"# {fexpect['name']}" not in readme:
            errors.append(f"README title mismatch for {fid}")
            
        # Check forbidden formatting
        if re.search(r"### .* \(.*\)", readme):
            errors.append(f"README {fid} uses forbidden '### Name (ID)' format")
        if re.search(r"- .* \(.*\)", readme):
            errors.append(f"README {fid} uses forbidden '- Name (ID)' format")
            
        for did, dexpect in fexpect["departments"].items():
            expected_h3 = f"### {did} {dexpect['name']}"
            if expected_h3 not in readme:
                errors.append(f"README {fid} missing correctly formatted department {did}: '{expected_h3}'")
            for uid, uname in dexpect["units"].items():
                expected_bullet = f"- {uid} {uname}"
                if expected_bullet not in readme:
                    errors.append(f"README {fid} missing correctly formatted unit {uid}: '{expected_bullet}'")

    if errors:
        for e in errors:
            print(e)
        print("FAIL")
        sys.exit(1)
    else:
        print("PASS: Family batch 165-174 expansion valid.")

if __name__ == "__main__":
    validate()
