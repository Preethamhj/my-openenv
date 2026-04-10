import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from env.environment import TASK_REGISTRY
from inference import run_task


def main():
    results = {"tasks": {}, "summary": {}}

    scores = []
    for task_name in ["easy", "medium", "hard", "expert"]:
        success, steps, score, rewards = run_task(task_name)
        results["tasks"][task_name] = {
            "success": success,
            "steps": steps,
            "score": round(score, 2),
            "rewards": [round(reward, 2) for reward in rewards],
            "num_stages": len(TASK_REGISTRY[task_name]["builder"](1)["stages"]),
        }
        scores.append(score)

    results["summary"] = {
        "average_score": round(sum(scores) / len(scores), 2),
        "task_count": len(scores),
        "deterministic_order": ["easy", "medium", "hard", "expert"],
    }

    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "baseline_results.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
