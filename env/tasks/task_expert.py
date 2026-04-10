def build_expert_scenario(difficulty_level: int) -> dict:
    affected_regions = ["us-east-1", "eu-west-1"]
    if difficulty_level > 1:
        affected_regions.append("ap-south-1")

    return {
        "task": "expert",
        "title": "Cloud control-plane compromise with identity containment",
        "difficulty_level": difficulty_level,
        "final_status": "identity blast radius contained and cloud access normalized",
        "stages": [
            {
                "name": "detect",
                "instruction": "Identify the primary cloud compromise indicators and suspicious identity activity.",
                "expected_keywords": ["iam", "access key", "privilege escalation", "sts"],
                "reasoning_keywords": ["control plane", "anomalous", "cross-region"],
                "completion_keywords": ["detect", "flag", "incident"],
                "penalty_keywords": ["benign", "normal activity"],
                "reward": {"partial": 0.2, "reasoning": 0.2, "completion": 0.2, "penalty": 0.1},
                "observation": {
                    "cloud_alert": {
                        "summary": "CloudTrail shows anomalous AssumeRole activity followed by IAM policy changes from a previously unseen access key.",
                        "events": [
                            "2026-04-08T03:11:08Z AssumeRole into OrganizationAccountAccessRole from access key AKIAZ9EXAMPLE",
                            "2026-04-08T03:12:14Z AttachUserPolicy AdministratorAccess to svc-backup-sync",
                            "2026-04-08T03:13:42Z CreateAccessKey for svc-backup-sync from 45.83.64.21",
                        ],
                        "affected_regions": affected_regions,
                        "false_positive_hint": "The backup sync role legitimately creates snapshots every night, but it should never receive AdministratorAccess or issue new access keys.",
                    }
                },
                "ordered_keywords_groups": [["assumerole", "sts", "access key"], ["privilege escalation", "administratoraccess"], ["incident", "flag"]],
                "requires_explanation": True,
            },
            {
                "name": "analyze",
                "instruction": "Explain likely attacker objectives, blast radius, and which cloud assets are most at risk.",
                "expected_keywords": ["privilege escalation", "exfiltration", "iam", "s3"],
                "reasoning_keywords": ["persistence", "multi-account", "secrets", "blast radius"],
                "completion_keywords": ["scope", "prioritize", "risk"],
                "penalty_keywords": ["low risk", "single event"],
                "reward": {"partial": 0.2, "reasoning": 0.2, "completion": 0.2, "penalty": 0.1},
                "observation": {
                    "business_context": {
                        "critical_assets": ["customer-data-archive", "terraform-state", "prod-secrets"],
                        "org_accounts": 6 + difficulty_level,
                        "customer_impact": "possible data exposure and control-plane persistence",
                        "tradeoff": "Aggressive IAM containment lowers exfiltration risk but may break deployment automation for 15 minutes.",
                    }
                },
                "ordered_keywords_groups": [["iam", "privilege escalation"], ["s3", "secrets", "multi-account"], ["risk", "scope"]],
                "requires_explanation": True,
            },
            {
                "name": "mitigate",
                "instruction": "Recommend the most urgent identity and access containment actions.",
                "expected_keywords": ["disable", "revoke", "rotate", "quarantine"],
                "reasoning_keywords": ["access key", "session", "policy", "scp"],
                "completion_keywords": ["contain", "block", "restrict", "isolate"],
                "penalty_keywords": ["leave active", "wait and watch"],
                "reward": {"partial": 0.15, "reasoning": 0.15, "completion": 0.3, "penalty": 0.1},
                "observation": {
                    "constraints": [
                        "Do not fully shut down production workloads.",
                        "Security leadership approved aggressive identity containment.",
                    ]
                },
                "ordered_keywords_groups": [["disable", "revoke"], ["quarantine", "contain"], ["scp", "restrict"]],
                "requires_explanation": True,
            },
            {
                "name": "recover",
                "instruction": "Describe recovery validation and long-term hardening steps.",
                "expected_keywords": ["audit", "mfa", "least privilege", "monitor"],
                "reasoning_keywords": ["forensics", "guardrails", "logging", "rotation"],
                "completion_keywords": ["recover", "validate", "rebuild trust", "review"],
                "penalty_keywords": ["resume immediately", "skip review"],
                "reward": {"partial": 0.15, "reasoning": 0.15, "completion": 0.35, "penalty": 0.1},
                "observation": {
                    "recovery_targets": ["iam users", "federation roles", "organization guardrails"],
                },
                "ordered_keywords_groups": [["audit", "forensics"], ["rotate", "mfa"], ["monitor", "review"]],
                "requires_explanation": True,
            },
        ],
    }
