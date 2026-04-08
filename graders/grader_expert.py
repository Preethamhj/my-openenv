def grade(pred: str, stage: dict) -> float:
    text = (pred or "").lower()
    score = 0.0

    if any(keyword.lower() in text for keyword in stage["expected_keywords"]):
        score += stage["reward"]["partial"]
    if any(keyword.lower() in text for keyword in stage["reasoning_keywords"]):
        score += stage["reward"]["reasoning"]
    if any(keyword.lower() in text for keyword in stage["completion_keywords"]):
        score += stage["reward"]["completion"]
    if any(keyword.lower() in text for keyword in stage["penalty_keywords"]):
        score -= stage["reward"]["penalty"]

    return min(max(score, 0.0), 1.0)
