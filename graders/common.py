from __future__ import annotations

import re


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _contains_any(text: str, keywords: list[str]) -> bool:
    normalized = _normalize(text)
    return any(keyword.lower() in normalized for keyword in keywords)


def _count_groups(text: str, keyword_groups: list[list[str]]) -> int:
    normalized = _normalize(text)
    matched = 0
    for group in keyword_groups:
        if any(keyword.lower() in normalized for keyword in group):
            matched += 1
    return matched


def score_stage(pred: str, stage: dict) -> float:
    text = _normalize(pred)
    reward = stage["reward"]
    score = 0.0

    if _contains_any(text, stage.get("expected_keywords", [])):
        score += reward["partial"]
    if _contains_any(text, stage.get("reasoning_keywords", [])):
        score += reward["reasoning"]
    if _contains_any(text, stage.get("completion_keywords", [])):
        score += reward["completion"]
    if _contains_any(text, stage.get("penalty_keywords", [])):
        score -= reward["penalty"]

    ordered_groups = stage.get("ordered_keywords_groups", [])
    if ordered_groups:
        matched_groups = _count_groups(text, ordered_groups)
        score += min(0.2, 0.05 * matched_groups)

    if stage.get("requires_explanation") and any(word in text for word in ["because", "due to", "so that", "which means"]):
        score += 0.05

    return min(max(score, 0.0), 1.0)
