from env.environment import CyberEnv


class CyberOpsClient:
    """Lightweight local client for interacting with the environment directly."""

    def __init__(self, task_name: str | None = None):
        self.env = CyberEnv(task_name=task_name)

    def reset(self):
        return self.env.reset()

    def step(self, action):
        return self.env.step(action)

    def state(self):
        return self.env.state()


__all__ = ["CyberOpsClient"]
