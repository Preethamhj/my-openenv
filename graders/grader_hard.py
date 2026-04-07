# Hard grader logic
def grade(pred):
    score = 0.0

    if "isolate" in pred.lower():
        score += 0.4
    if "revoke" in pred.lower():
        score += 0.3
    if "patch" in pred.lower():
        score += 0.3

    return min(score, 1.0)