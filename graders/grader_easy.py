# Easy grader logic
def grade(pred):
    if "192.168.1.10" in pred:
        return 1.0
    elif pred:
        return 0.5
    return 0.0