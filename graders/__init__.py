from graders.grader_easy import grade as grade_easy
from graders.grader_expert import grade as grade_expert
from graders.grader_hard import grade as grade_hard
from graders.grader_medium import grade as grade_medium

GRADERS = {
    "easy": grade_easy,
    "medium": grade_medium,
    "hard": grade_hard,
    "expert": grade_expert,
}

__all__ = [
    "GRADERS",
    "grade_easy",
    "grade_medium",
    "grade_hard",
    "grade_expert",
]
