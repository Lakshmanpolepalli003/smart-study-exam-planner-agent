import json
import datetime
from pathlib import Path
from typing import List, Dict, Any
from google.adk.agents import Agent

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
PROGRESS_FILE = DATA_DIR / "progress.json"

def _load_progress():
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"sessions": []}

def _save_progress(progress):
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))

def generate_study_plan(subjects, hours_per_day, exam_date, difficulty):
    today = datetime.date.today()
    exam = datetime.date.fromisoformat(exam_date)
    days_left = max((exam - today).days, 1)

    base_per = hours_per_day / len(subjects)
    diff_weight = {"easy": 0.8, "medium": 1.0, "hard": 1.3}

    schedule = []
    for sub in subjects:
        level = difficulty.get(sub, "medium")
        hours = round(base_per * diff_weight[level], 2)
        schedule.append({
            "subject": sub,
            "difficulty": level,
            "hours_per_day": hours,
            "days_left": days_left,
        })

    plan = {
        "generated_on": today.isoformat(),
        "exam_date": exam_date,
        "hours_per_day": hours_per_day,
        "schedule": schedule,
    }

    p = _load_progress()
    p["last_plan"] = plan
    _save_progress(p)

    return plan

def log_daily_progress(date, completed_subjects, notes=""):
    p = _load_progress()
    p["sessions"].append({
        "date": date,
        "completed_subjects": completed_subjects,
        "notes": notes,
    })
    _save_progress(p)
    return p

def generate_revision_quiz(subject, topic):
    return {
        "instruction": f"Generate a 5-question quiz for {subject} – topic: {topic}"
    }

root_agent = Agent(
    name="smart_study_exam_planner",
    model="gemini-2.0-flash",
    description="Study planner agent for students",
    instruction="Use the tools to generate study plans, track progress, and build quizzes.",
    tools=[generate_study_plan, log_daily_progress, generate_revision_quiz],
)
