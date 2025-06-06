import os
from datetime import datetime

HIGHSCORE_FILE = "highscores.txt"

def save_high_score(score):
    now = datetime.now().strftime("%Y-%m-%d")
    scores = load_high_scores(raw=True)
    scores.append((score, now))
    # Sort by score descending, keep top 10
    scores = sorted(scores, key=lambda x: x[0], reverse=True)[:10]
    with open(HIGHSCORE_FILE, "w") as f:
        for s, date in scores:
            f.write(f"{s},{date}\n")

def load_high_scores(limit=10, raw=False):
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    with open(HIGHSCORE_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    scores = []
    for line in lines:
        parts = line.split(",")
        if len(parts) == 2 and parts[0].isdigit():
            scores.append((int(parts[0]), parts[1]))
    if raw:
        return scores
    return scores[:limit]
