def build_easy_scenario(difficulty_level: int) -> dict:
    noisy_login_count = 3 + difficulty_level
    noise_logs = [
        "2026-04-07T08:14:02Z auth.info bastion sshd[4312]: Accepted publickey for analyst from 10.0.4.22 port 50211",
        "2026-04-07T08:14:29Z auth.warn bastion sshd[4319]: Failed password for invalid user backup from 203.0.113.77 port 44321",
        "2026-04-07T08:15:11Z auth.info vpn openvpn[220]: Peer Connection Initiated with [AF_INET]198.51.100.23:1194",
    ]
    suspicious_logs = [
        "2026-04-07T08:16:04Z auth.warn bastion sshd[4401]: Failed password for root from 185.199.110.17 port 51128",
        "2026-04-07T08:16:09Z auth.warn bastion sshd[4402]: Failed password for root from 185.199.110.17 port 51134",
        "2026-04-07T08:16:15Z auth.warn bastion sshd[4405]: Failed password for root from 185.199.110.17 port 51141",
        "2026-04-07T08:16:23Z auth.warn bastion sshd[4409]: Failed password for deploy from 185.199.110.17 port 51163",
    ][: noisy_login_count]

    return {
        "task": "easy",
        "title": "Credential stuffing triage on the bastion host",
        "difficulty_level": difficulty_level,
        "final_status": "monitoring enabled after access controls updated",
        "stages": [
            {
                "name": "detect",
                "instruction": "Identify the suspicious source or anomaly in the authentication logs.",
                "expected_keywords": ["185.199.110.17", "failed", "suspicious"],
                "reasoning_keywords": ["brute force", "credential stuffing", "repeated"],
                "completion_keywords": ["identify", "detect", "flag", "block"],
                "penalty_keywords": ["allow", "ignore", "safe"],
                "ordered_keywords_groups": [["185.199.110.17"], ["brute force", "credential stuffing"], ["block", "flag"]],
                "requires_explanation": True,
                "reward": {"partial": 0.25, "reasoning": 0.2, "completion": 0.25, "penalty": 0.15},
                "observation": {
                    "alert": "SOC triage alert: repeated SSH authentication failures on bastion-1.",
                    "logs": noise_logs + suspicious_logs,
                    "suspected_asset": "bastion-1",
                },
            },
            {
                "name": "prioritize",
                "instruction": "Explain why this activity matters and prioritize the response.",
                "expected_keywords": ["high priority", "critical", "bastion"],
                "reasoning_keywords": ["internet-facing", "root", "lateral movement"],
                "completion_keywords": ["escalate", "contain", "ticket", "priority"],
                "penalty_keywords": ["low priority", "close alert"],
                "ordered_keywords_groups": [["internet-facing", "bastion"], ["root", "lateral movement"], ["escalate", "contain"]],
                "requires_explanation": True,
                "reward": {"partial": 0.2, "reasoning": 0.2, "completion": 0.25, "penalty": 0.1},
                "observation": {
                    "context": {
                        "asset_exposure": "internet-facing jump host",
                        "business_owner": "platform engineering",
                        "failed_login_count": noisy_login_count + 1,
                    }
                },
            },
            {
                "name": "mitigate",
                "instruction": "Recommend the next containment action and recovery check.",
                "expected_keywords": ["block", "185.199.110.17", "reset"],
                "reasoning_keywords": ["mfa", "credential", "review", "firewall"],
                "completion_keywords": ["monitor", "recover", "rotate", "reset"],
                "penalty_keywords": ["do nothing", "reboot only"],
                "ordered_keywords_groups": [["block"], ["reset", "rotate"], ["monitor", "review"]],
                "requires_explanation": True,
                "reward": {"partial": 0.2, "reasoning": 0.15, "completion": 0.35, "penalty": 0.1},
                "observation": {
                    "constraints": [
                        "Keep bastion service available for engineers.",
                        "Do not interrupt the CI deployment window.",
                    ]
                },
            },
        ],
    }
