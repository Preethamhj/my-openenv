def build_medium_scenario(difficulty_level: int) -> dict:
    extra_assets = ["payments-api"] if difficulty_level > 1 else []
    return {
        "task": "medium",
        "title": "Vulnerability triage for exposed application servers",
        "difficulty_level": difficulty_level,
        "final_status": "patch window approved with compensating controls active",
        "stages": [
            {
                "name": "detect",
                "instruction": "Review the vulnerability bulletin and identify the highest-risk issue.",
                "expected_keywords": ["cve-2026-44210", "critical", "remote code execution"],
                "reasoning_keywords": ["internet-facing", "unauthenticated", "exploit"],
                "completion_keywords": ["prioritize", "critical", "patch"],
                "penalty_keywords": ["ignore", "informational"],
                "reward": {"partial": 0.25, "reasoning": 0.2, "completion": 0.25, "penalty": 0.15},
                "observation": {
                    "report": [
                        {
                            "asset": "edge-gateway-2",
                            "cve": "CVE-2026-44210",
                            "severity": "critical",
                            "cvss": 9.8,
                            "vector": "unauthenticated remote code execution in VPN gateway",
                        },
                        {
                            "asset": "inventory-db",
                            "cve": "CVE-2025-11990",
                            "severity": "medium",
                            "cvss": 5.4,
                            "vector": "local information disclosure",
                        },
                    ],
                    "related_assets": ["edge-gateway-2", "sso-proxy"] + extra_assets,
                },
            },
            {
                "name": "prioritize",
                "instruction": "Explain blast radius, business impact, and priority.",
                "expected_keywords": ["vpn", "external", "high priority"],
                "reasoning_keywords": ["lateral movement", "customer access", "blast radius"],
                "completion_keywords": ["escalate", "change window", "owner"],
                "penalty_keywords": ["defer", "next quarter"],
                "reward": {"partial": 0.2, "reasoning": 0.2, "completion": 0.25, "penalty": 0.1},
                "observation": {
                    "business_context": {
                        "service": "remote workforce VPN",
                        "criticality": "tier-0 access path",
                        "active_users": 1800 + (200 * difficulty_level),
                    }
                },
            },
            {
                "name": "mitigate",
                "instruction": "Recommend mitigation, validation, and monitoring actions.",
                "expected_keywords": ["patch", "restrict", "vpn", "monitor"],
                "reasoning_keywords": ["waf", "ip allowlist", "validate"],
                "completion_keywords": ["rollback", "scan", "verify", "deploy"],
                "penalty_keywords": ["wait", "accept risk"],
                "reward": {"partial": 0.2, "reasoning": 0.15, "completion": 0.35, "penalty": 0.1},
                "observation": {
                    "constraints": [
                        "Downtime must remain under 10 minutes.",
                        "Executives require an update before the maintenance window starts.",
                    ]
                },
            },
        ],
    }
