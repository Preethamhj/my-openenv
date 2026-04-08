from env.tasks.task_easy import build_easy_scenario
from env.tasks.task_expert import build_expert_scenario
from env.tasks.task_hard import build_hard_scenario
from env.tasks.task_medium import build_medium_scenario

TASK_BUILDERS = {
    "easy": build_easy_scenario,
    "medium": build_medium_scenario,
    "hard": build_hard_scenario,
    "expert": build_expert_scenario,
}

__all__ = [
    "TASK_BUILDERS",
    "build_easy_scenario",
    "build_medium_scenario",
    "build_hard_scenario",
    "build_expert_scenario",
]
