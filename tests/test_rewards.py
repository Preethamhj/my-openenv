import unittest

from graders.grader_expert import grade as grade_expert
from graders.grader_hard import grade as grade_hard
from env.tasks.task_expert import build_expert_scenario
from env.tasks.task_hard import build_hard_scenario


class RewardTests(unittest.TestCase):
    def test_hard_reward_stays_bounded(self):
        stage = build_hard_scenario(1)["stages"][0]
        score = grade_hard(
            "powershell credential theft because this is ransomware and we should isolate now",
            stage,
        )
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_expert_reward_prefers_reasoned_sequence(self):
        stage = build_expert_scenario(1)["stages"][0]
        score = grade_expert(
            "Detect anomalous AssumeRole and access key privilege escalation because this control plane event indicates an incident.",
            stage,
        )
        self.assertGreaterEqual(score, 0.45)


if __name__ == "__main__":
    unittest.main()
