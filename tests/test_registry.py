import unittest

from env.environment import CyberEnv, TASK_REGISTRY
from graders import GRADERS


class RegistryTests(unittest.TestCase):
    def test_task_registry_has_matching_graders(self):
        self.assertGreaterEqual(len(TASK_REGISTRY), 3)
        self.assertTrue(set(TASK_REGISTRY.keys()).issubset(set(GRADERS.keys())))

    def test_environment_can_reset_specific_task(self):
        env = CyberEnv(task_name="hard")
        obs = env.reset()
        self.assertEqual(obs.task, "hard")
        self.assertEqual(obs.data.stage_name, "detect")


if __name__ == "__main__":
    unittest.main()
