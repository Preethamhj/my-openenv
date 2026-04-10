from env.environment import CyberEnv


class CyberOpsClient:
    """Lightweight local client for interacting with the environment directly."""

    def __init__(self, task_name: str | None = None):
        self.env = CyberEnv(task_name=task_name)

    def reset(self, task: str | None = None):
        return self.env.reset(task=task)

    def step(self, action):
        return self.env.step(action)

    def state(self):
        return self.env.state()

    def trace(self):
        return {
            "task": self.env.task,
            "done": self.env.done,
            "history": self.env.history,
        }


__all__ = ["CyberOpsClient"]
