# Environment logic for your-openenv-project
import random

from models.observation import Observation
from models.reward import Reward

from graders.grader_easy import grade as grade_easy
from graders.grader_medium import grade as grade_medium
from graders.grader_hard import grade as grade_hard


class CyberEnv:
    def __init__(self):
        self.task = ""
        self.done = False

    def reset(self):
        self.done = False
        self.task = random.choice(["easy", "medium", "hard"])

        if self.task == "easy":
            data = {"logs": ["Failed login from 192.168.1.10"]}
        elif self.task == "medium":
            data = {"cve": ["CVE-2024-1234 high severity"]}
        else:
            data = {"incident": "Server breached"}

        return Observation(task=self.task, data=data)

    def step(self, action):
        text = action.get("action", "")

        if self.task == "easy":
            score = grade_easy(text)
        elif self.task == "medium":
            score = grade_medium(text)
        else:
            score = grade_hard(text)

        reward = max(0.0, min(1.0, score))

        if reward >= 0.9:
            self.done = True

        return (
            Observation(task=self.task, data={"status": "continue"}),
            reward,
            self.done,
            {}
        )

    def state(self):
        return {"task": self.task, "done": self.done}