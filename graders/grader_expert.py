from graders.common import score_stage


def grade(pred: str, stage: dict) -> float:
    return score_stage(pred, stage)
