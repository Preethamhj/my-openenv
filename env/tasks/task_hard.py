def build_hard_scenario(difficulty_level: int) -> dict:
    impacted_hosts = ["payments-db-1", "payments-api-2", "vault-proxy"]
    if difficulty_level > 1:
        impacted_hosts.append("partner-sftp")

    return {
        "task": "hard",
        "title": "Ransomware precursor investigation with containment and recovery",
        "difficulty_level": difficulty_level,
        "final_status": "threat contained, credentials rotated, and recovery initiated",
        "stages": [
            {
                "name": "detect",
                "instruction": "Identify the active incident and the most urgent compromise indicators.",
                "expected_keywords": ["ransomware", "credential theft", "powershell", "encrypted"],
                "reasoning_keywords": ["domain admin", "lateral movement", "c2"],
                "completion_keywords": ["isolate", "contain", "incident"],
                "penalty_keywords": ["false positive", "benign"],
                "ordered_keywords_groups": [["powershell", "credential theft"], ["encrypted", "ransomware"], ["isolate", "contain"]],
                "requires_explanation": True,
                "reward": {"partial": 0.2, "reasoning": 0.2, "completion": 0.2, "penalty": 0.1},
                "observation": {
                    "incident": {
                        "summary": "EDR flagged credential dumping followed by suspicious encryption activity in the payments segment.",
                        "indicators": [
                            "2026-04-07T11:02:14Z WIN-PRD-22 powershell.exe invoked mimikatz-like command line",
                            "2026-04-07T11:04:50Z payments-db-1 SMB writes created *.locked files",
                            "2026-04-07T11:05:13Z vault-proxy outbound connection to 45.83.64.21:8443",
                        ],
                        "impacted_hosts": impacted_hosts,
                    }
                },
            },
            {
                "name": "analyze",
                "instruction": "Explain attacker path, likely objectives, and affected business services.",
                "expected_keywords": ["payments", "domain admin", "lateral movement"],
                "reasoning_keywords": ["credential dumping", "smb", "exfiltration", "blast radius"],
                "completion_keywords": ["scope", "timeline", "priority"],
                "penalty_keywords": ["single host only", "no impact"],
                "ordered_keywords_groups": [["payments"], ["lateral movement", "blast radius"], ["scope", "priority"]],
                "requires_explanation": True,
                "reward": {"partial": 0.2, "reasoning": 0.2, "completion": 0.2, "penalty": 0.1},
                "observation": {
                    "business_context": {
                        "critical_service": "card payment processing",
                        "revenue_risk_per_hour": 120000 + (15000 * difficulty_level),
                        "customer_impact": "checkout failures and delayed settlements",
                    }
                },
            },
            {
                "name": "mitigate",
                "instruction": "Recommend containment and eradication actions in priority order.",
                "expected_keywords": ["isolate", "revoke", "disable", "block"],
                "reasoning_keywords": ["segmentation", "ioc", "credential rotation"],
                "completion_keywords": ["edr", "firewall", "disable", "quarantine"],
                "penalty_keywords": ["leave online", "monitor only"],
                "ordered_keywords_groups": [["isolate"], ["revoke", "disable"], ["block", "quarantine"]],
                "requires_explanation": True,
                "reward": {"partial": 0.15, "reasoning": 0.15, "completion": 0.3, "penalty": 0.1},
                "observation": {
                    "constraints": [
                        "The incident commander approved aggressive containment.",
                        "Preserve forensic evidence where possible.",
                    ]
                },
            },
            {
                "name": "recover",
                "instruction": "Describe recovery, validation, and long-term hardening steps.",
                "expected_keywords": ["restore", "validate", "patch", "monitor"],
                "reasoning_keywords": ["backup", "forensics", "lessons learned"],
                "completion_keywords": ["recover", "rotate", "rebuild", "mfa"],
                "penalty_keywords": ["resume immediately", "skip validation"],
                "ordered_keywords_groups": [["restore"], ["validate", "forensics"], ["rotate", "mfa"]],
                "requires_explanation": True,
                "reward": {"partial": 0.15, "reasoning": 0.15, "completion": 0.35, "penalty": 0.1},
                "observation": {
                    "recovery_targets": impacted_hosts,
                },
            },
        ],
    }
