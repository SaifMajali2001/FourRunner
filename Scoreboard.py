import json
import os

SCORES_FILE = "scores.json"
MAX_SCORES  = 8

def load_scores():
    """Load scores from file. Returns a sorted list of times (floats, ascending)."""
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, "r") as f:
            data = json.load(f)
            return sorted(data)
    except (json.JSONDecodeError, ValueError):
        return []

def save_score(elapsed_seconds):
    """Add a new score, keep only the top 8 best (lowest) times, and save."""
    scores = load_scores()
    scores.append(elapsed_seconds)
    scores = sorted(scores)[:MAX_SCORES]
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)
    return scores