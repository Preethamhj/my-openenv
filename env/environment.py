import random

from models.observation import Observation

from graders.grader_easy import grade as grade_easy
from graders.grader_expert import grade as grade_expert
from graders.grader_medium import grade as grade_medium
from graders.grader_hard import grade as grade_hard
from env.tasks.task_easy import build_easy_scenario
from env.tasks.task_expert import build_expert_scenario
from env.tasks.task_medium import build_medium_scenario
from env.tasks.task_hard import build_hard_scenario

TASK_REGISTRY = {
    "easy": {"builder": build_easy_scenario, "grader": grade_easy},
    "medium": {"builder": build_medium_scenario, "grader": grade_medium},
    "hard": {"builder": build_hard_scenario, "grader": grade_hard},
    "expert": {"builder": build_expert_scenario, "grader": grade_expert},
}


class CyberEnv:
    def __init__(self, task_name: str | None = None):
        self.task = ""
        self.done = False
        self.history = []
        self.stage_index = 0
        self.current_scenario = {}
        self.performance_signal = 0
        self.task_name = task_name

    def _difficulty_level(self) -> int:
        if self.performance_signal >= 2:
            return 2
        if self.performance_signal <= -2:
            return 0
        return 1

    def _build_scenario(self, task_name: str) -> dict:
        difficulty_level = self._difficulty_level()
        return TASK_REGISTRY[task_name]["builder"](difficulty_level)

    def _current_stage(self) -> dict:
        return self.current_scenario["stages"][self.stage_index]

    def _build_observation(self) -> Observation:
        stage = self._current_stage()
        completed_stages = self.stage_index
        total_stages = len(self.current_scenario["stages"])
        progress = round(completed_stages / total_stages, 2)

        data = {
            "title": self.current_scenario["title"],
            "difficulty_level": self.current_scenario["difficulty_level"],
            "step": self.stage_index + 1,
            "progress": progress,
            "stage_name": stage["name"],
            "instruction": stage["instruction"],
            "history": list(self.history),
        }
        data.update(stage["observation"])

        return Observation(task=self.task, data=data)

    def reset(self):
        self.done = False
        self.history = []
        self.stage_index = 0
        available_tasks = list(TASK_REGISTRY.keys())
        self.task = self.task_name or random.choice(available_tasks)
        self.current_scenario = self._build_scenario(self.task)
        return self._build_observation()

    def step(self, action):
        text = action.get("action", "")
        stage = self._current_stage()

        reward = TASK_REGISTRY[self.task]["grader"](text, stage)

        self.history.append(
            {
                "step": self.stage_index + 1,
                "stage": stage["name"],
                "action": text,
                "reward": round(reward, 2),
            }
        )

        stage_complete = reward >= 0.4
        if stage_complete and self.stage_index < len(self.current_scenario["stages"]) - 1:
            self.stage_index += 1
        elif stage_complete:
            self.done = True

        if self.done:
            self.performance_signal = min(self.performance_signal + 1, 3)
            next_observation = Observation(
                task=self.task,
                data={
                    "title": self.current_scenario["title"],
                    "step": len(self.current_scenario["stages"]),
                    "progress": 1.0,
                    "history": list(self.history),
                    "status": self.current_scenario["final_status"],
                },
            )
        else:
            if reward < 0.2:
                self.performance_signal = max(self.performance_signal - 1, -3)
            next_observation = self._build_observation()

        return next_observation, min(max(reward, 0.0), 1.0), self.done, {}

    def state(self):
        return {
            "task": self.task,
            "done": self.done,
            "step": self.stage_index + 1 if self.current_scenario else 0,
            "history": list(self.history),
            "difficulty_level": self.current_scenario.get("difficulty_level", 1),
        }


__all__ = ["CyberEnv", "TASK_REGISTRY"]
