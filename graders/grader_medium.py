# Medium grader logic
def grade(pred):
    if "critical" in pred.lower():
        return 1.0
    elif pred:
        return 0.5
    return 0.0