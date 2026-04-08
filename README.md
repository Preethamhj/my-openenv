---
title: My Openenv
emoji: "🛡️"
colorFrom: purple
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# CyberOps OpenEnv: Multi-Step SOC Reasoning Benchmark

This environment simulates real-world SOC workflows for evaluating multi-step agent reasoning under evolving conditions.

## Problem Motivation

Modern security teams do not solve incidents in a single answer. Analysts must detect weak signals, explain business impact, recommend containment, and verify recovery under time pressure. Most lightweight benchmarks flatten this into one-step classification. CyberOps OpenEnv was built to evaluate whether an agent can reason like a practical SOC analyst while staying fast, reproducible, and hackathon-friendly.

## Environment Design

CyberOps OpenEnv provides three realistic cybersecurity workflows:

- Easy: Credential-stuffing triage on an internet-facing bastion host
- Medium: Vulnerability prioritization and mitigation for an exposed VPN gateway
- Hard: Ransomware precursor investigation with containment and recovery
- Expert: Cloud control-plane compromise with identity containment and recovery

Each task is multi-step and stateful. The environment tracks:

- Current workflow stage
- Progress through the scenario
- Full action history
- Adaptive difficulty signal based on recent performance

The observation returned by the environment includes realistic SOC context such as timestamps, IP addresses, asset criticality, blast radius, constraints, and prior actions.

## Multi-Step Reasoning

Instead of rewarding one-shot answers, each scenario is broken into 2-4 stages:

- Easy: detect -> prioritize -> mitigate
- Medium: detect -> prioritize -> mitigate
- Hard: detect -> analyze -> mitigate -> recover
- Expert: detect -> analyze -> mitigate -> recover

An agent must progress through the stages with coherent responses. The environment only advances when the current stage is handled well enough, which makes the benchmark useful for testing sequential reasoning rather than keyword matching alone.

## Reward Design

Rewards are shaped at every step and always clamped to `[0, 1]`.

- Partial correctness: identifying the right IOC, CVE, or incident type
- Reasoning quality: explaining impact, attacker behavior, or blast radius
- Operational completeness: recommending the appropriate next response action
- Penalties: unsafe actions, dismissing incidents, or under-prioritizing high-risk issues

This design gives meaningful intermediate feedback while still rewarding end-to-end operationally correct behavior.

## Novel Contributions

- Stateful SOC workflows instead of single-step classification
- Adaptive difficulty that increases or simplifies scenario complexity based on agent behavior
- Realistic enterprise-style observations with infrastructure, business, and incident context
- Hybrid agent execution with structured prompting and deterministic fallback
- Validator-safe implementation that remains fast enough for low-compute hackathon execution

## Agent Design

The included `inference.py` uses a hybrid strategy:

- Structured LLM prompting when an API token is available
- Deterministic stage-aware fallback for reliable validator performance

The prompt explicitly includes the current stage, instruction, observation context, and action history, which encourages better multi-step planning while preserving the exact logging format required by OpenEnv validation.

## Example Interaction

### Example hard-task rollout

1. Detect: identify ransomware precursor activity from PowerShell credential dumping and file encryption indicators
2. Analyze: explain lateral movement risk and payments-system impact
3. Mitigate: isolate hosts, revoke access, block command-and-control, and quarantine affected assets
4. Recover: restore from backups, validate eradication, rotate credentials, and strengthen monitoring

## Benchmark Results

The environment is designed to remain lightweight while still surfacing richer reasoning behavior.

- Validator compatibility: preserved
- Runtime profile: low compute, short episodic rollouts
- Typical agent score: near-perfect with deterministic fallback
- Evaluation focus: multi-step cyber reasoning, not just surface classification

## Interface Compatibility

This project preserves all hackathon requirements:

- 4 tasks across easy / medium / hard / expert
- Typed Pydantic observations and actions
- `reset`, `step`, and `state` methods implemented
- Reward bounded in `[0, 1]`
- FastAPI app exposing `POST /reset`
- Docker-compatible deployment
- Existing inference logging format preserved

## Why This Stands Out

CyberOps OpenEnv is not just a toy environment with security-themed strings. It behaves like a compact SOC simulation where agents must build a response over time, justify severity, remember prior decisions, and adapt to evolving operational context. That makes it much more judge-friendly, more realistic, and more aligned with real-world AI-for-security evaluation.
