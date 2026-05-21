"""
Demo script — creates sample tasks and calls the API endpoints.
Run the API first: python app.py
Then in another terminal: python demo.py
"""

import requests
import json

BASE = "http://localhost:5000"

def pretty(r):
    print(json.dumps(r.json(), indent=2))
    print()

print("=== AI Task API Demo ===\n")

# Create tasks
sample_tasks = [
    {"title": "Fix critical crash in payment endpoint", "description": "Users are getting 500 errors on checkout, urgent fix needed"},
    {"title": "Train ML model for churn prediction", "description": "Build and evaluate a model on the user dataset"},
    {"title": "Design onboarding flow mockup", "description": "Figma wireframes for new user onboarding"},
    {"title": "Write Q2 roadmap document", "description": "Plan features for next quarter, schedule review meeting"},
    {"title": "Deploy new backend API to staging", "description": "Docker build and push, update CI pipeline"},
]

print("Creating tasks...\n")
ids = []
for t in sample_tasks:
    r = requests.post(f"{BASE}/tasks", json=t)
    task = r.json()["task"]
    ids.append(task["id"])
    print(f"  [{task['priority'].upper():6}] [{task['category']:12}] {task['title']}")

print("\n--- Priority Summary ---")
pretty(requests.get(f"{BASE}/tasks/summary"))

print("--- High Priority Tasks ---")
pretty(requests.get(f"{BASE}/tasks?priority=high"))
