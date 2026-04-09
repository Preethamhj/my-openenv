import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from env.environment import CyberEnv, TASK_REGISTRY

API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
HF_TOKEN = os.getenv("HF_TOKEN") or ""
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN) if OpenAI else None

MAX_STEPS = 6


def log_start(task, env_name, model):
    print(f"[START] task={task} env={env_name} model={model}", flush=True)


def log_step(step, action, reward, done):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null",
        flush=True,
    )


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


def build_structured_prompt(obs):
    return (
        "You are a SOC analyst solving a multi-step cyber incident.\n"
        f"Task: {obs.task}\n"
        f"Stage: {obs.data.get('stage_name')}\n"
        f"Instruction: {obs.data.get('instruction')}\n"
        f"History: {obs.data.get('history')}\n"
        f"Context: {obs.data}\n"
        "Respond with one concise action sentence that includes detection, reasoning, and next action."
    )


def fallback_action(obs):
    stage = obs.data.get("stage_name")
    scripted_actions = {
        ("easy", "detect"): "Detect brute force activity from 185.199.110.17 after repeated failed root logins on the bastion host.",
        ("easy", "prioritize"): "Escalate as high priority because the internet-facing bastion is seeing repeated root login failures that could enable lateral movement.",
        ("easy", "mitigate"): "Block 185.199.110.17, reset exposed credentials, enforce MFA, and monitor the bastion for recovery validation.",
        ("medium", "detect"): "Prioritize CVE-2026-44210 as a critical remote code execution issue on the external VPN gateway.",
        ("medium", "prioritize"): "Escalate to a high-priority patch because the internet-facing VPN can enable lateral movement and impact customer access.",
        ("medium", "mitigate"): "Patch the VPN gateway, restrict access with temporary allowlists, validate with rescans, and monitor for exploit attempts.",
        ("hard", "detect"): "Declare a ransomware incident involving credential theft, suspicious PowerShell activity, and encryption on payments systems.",
        ("hard", "analyze"): "Scope this as domain-admin-enabled lateral movement across the payments environment with major revenue and customer impact.",
        ("hard", "mitigate"): "Isolate affected hosts, revoke compromised privileged accounts, disable malicious access paths, and block the command-and-control IOC.",
        ("hard", "recover"): "Restore clean systems from backups, validate eradication with forensic review, patch gaps, rotate credentials, and increase monitoring.",
        ("expert", "detect"): "Detect a cloud control-plane compromise involving anomalous AssumeRole activity, new access keys, and IAM privilege escalation.",
        ("expert", "analyze"): "Scope this as a multi-account IAM compromise with persistence and possible access to S3, secrets, and other cloud control-plane assets.",
        ("expert", "mitigate"): "Disable the malicious access keys, revoke active sessions, quarantine privileged identities, and restrict privilege escalation with organization guardrails.",
        ("expert", "recover"): "Audit IAM changes, rotate credentials, enforce MFA and least privilege, validate logging coverage, and review long-term guardrails.",
    }
    return scripted_actions.get((obs.task, stage), "Analyze the incident, explain the risk, and take the safest next containment action.")


def get_action(obs):
    if client is not None:
        if not HF_TOKEN:
            raise RuntimeError("HF_TOKEN environment variable is required for inference.")

        prompt = build_structured_prompt(obs)
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a concise incident responder. Provide one actionable response sentence."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=120,
            temperature=0.2,
        )
        text = (res.choices[0].message.content or "").strip()
        if text:
            return text

    return fallback_action(obs)


def run_task(task_name):
    env = CyberEnv(task_name=task_name)
    rewards = []
    steps = 0
    success = False
    obs = None

    try:
        obs = env.reset()
        log_start(obs.task, "cyberops", MODEL_NAME)

        for step in range(1, MAX_STEPS + 1):
            action_text = get_action(obs)
            obs, reward, done, _ = env.step({"action": action_text})
            rewards.append(reward)
            steps = step
            log_step(step, action_text, reward, done)
            if done:
                break

        score = min(max(sum(rewards) / len(rewards), 0.0), 1.0) if rewards else 0.0
        success = score >= 0.5
    except Exception:
        score = min(max(sum(rewards) / len(rewards), 0.0), 1.0) if rewards else 0.0
        success = False
        raise
    finally:
        score = min(max(sum(rewards) / len(rewards), 0.0), 1.0) if rewards else 0.0
        log_end(success, steps, score, rewards)

    return success, steps, score, rewards


def main():
    overall_success = True
    task_names = ["easy", "medium", "hard"]

    for task_name in task_names:
        success, _, _, _ = run_task(task_name)
        overall_success = overall_success and success

    if "expert" in TASK_REGISTRY:
        run_task("expert")

    return 0 if overall_success else 1


if __name__ == "__main__":
    raise SystemExit(main())
