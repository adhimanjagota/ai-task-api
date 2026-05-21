"""
Rule-based AI task prioritizer.
Assigns priority scores based on urgency signals and category weights.
"""

URGENCY_KEYWORDS = {
    "high": ["urgent", "asap", "critical", "blocker", "immediately",
             "broken", "down", "crash", "emergency", "deadline", "today"],
    "low":  ["someday", "nice to have", "low priority", "eventually",
             "when possible", "optional", "minor", "later"],
}

CATEGORY_BASE_SCORES = {
    "engineering": 60,
    "data":        55,
    "product":     50,
    "design":      45,
    "operations":  40,
    "general":     35,
}


class TaskPrioritizer:
    def score(self, title: str, description: str, category: str) -> dict:
        text = (title + " " + description).lower()
        base = CATEGORY_BASE_SCORES.get(category, 35)

        bonus = 0
        for kw in URGENCY_KEYWORDS["high"]:
            if kw in text:
                bonus += 15

        penalty = 0
        for kw in URGENCY_KEYWORDS["low"]:
            if kw in text:
                penalty += 10

        final = min(100, max(0, base + bonus - penalty))

        if final >= 70:
            label = "high"
        elif final >= 45:
            label = "medium"
        else:
            label = "low"

        return {"score": final, "label": label}
