"""
Rule-based AI task classifier.
Categorizes tasks by analyzing keywords in title and description.
"""

from typing import Tuple

CATEGORY_RULES = {
    "engineering": [
        "bug", "fix", "deploy", "api", "database", "server", "code",
        "test", "build", "refactor", "pipeline", "endpoint", "backend",
        "frontend", "migration", "docker", "ci", "cd", "error", "crash"
    ],
    "design": [
        "ui", "ux", "design", "mockup", "wireframe", "prototype",
        "figma", "layout", "color", "font", "logo", "icon", "visual"
    ],
    "data": [
        "data", "model", "train", "dataset", "ml", "ai", "predict",
        "analysis", "analytics", "chart", "dashboard", "report",
        "metric", "experiment", "feature", "accuracy"
    ],
    "product": [
        "feature", "roadmap", "launch", "release", "user story",
        "requirement", "spec", "feedback", "onboarding", "flow"
    ],
    "operations": [
        "meeting", "call", "email", "review", "document", "write",
        "schedule", "plan", "coordinate", "update", "send", "follow up"
    ],
}


class TaskClassifier:
    def classify(self, title: str, description: str = "") -> str:
        text = (title + " " + description).lower()
        scores = {cat: 0 for cat in CATEGORY_RULES}
        for category, keywords in CATEGORY_RULES.items():
            for kw in keywords:
                if kw in text:
                    scores[category] += 1
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "general"
