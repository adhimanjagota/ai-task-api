# AI Task API
 
A backend REST API that uses AI-powered classification and prioritization to automatically organize tasks. Built with Python and Flask — cloud-ready, modular, and extensible.
 
---
 
## What it does
 
- Accepts tasks via REST API and **auto-classifies** them into categories (engineering, data, design, product, operations)
- **Scores and prioritizes** each task using urgency signal detection and category weighting
- Full CRUD API — create, read, update, delete tasks
- Filter tasks by category or priority
- Returns an AI-generated summary of your task pipeline
---
 
## Demo output
 
```
=== AI Task API Demo ===
 
Creating tasks...
 
  [HIGH  ] [engineering ] Fix critical crash in payment endpoint
  [MEDIUM] [data        ] Train ML model for churn prediction
  [MEDIUM] [design      ] Design onboarding flow mockup
  [LOW   ] [operations  ] Write Q2 roadmap document
  [MEDIUM] [engineering ] Deploy new backend API to staging
 
--- Priority Summary ---
{
  "by_category": {
    "data": 1,
    "design": 1,
    "engineering": 2,
    "operations": 1
  },
  "by_priority": {
    "high": 1,
    "low": 1,
    "medium": 3
  },
  "done": 0,
  "in_progress": 0,
  "pending": 5,
  "top_priority": ["Fix critical crash in payment endpoint"],
  "total_tasks": 5
}
 
--- High Priority Tasks ---
{
  "count": 1,
  "tasks": [
    {
      "category": "engineering",
      "id": "0b343dec",
      "priority": "high",
      "priority_score": 100,
      "status": "pending",
      "title": "Fix critical crash in payment endpoint"
    }
  ]
}
```
 
---
 
## How to run
 
```bash
git clone https://github.com/adhimanjagota/ai-task-api.git
cd ai-task-api
pip install -r requirements.txt
 
# Terminal 1 — start the API
python app.py
 
# Terminal 2 — run the demo
python demo.py
```
 
---
 
## API endpoints
 
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info and endpoint list |
| GET | `/tasks` | List all tasks (filter by `?category=` or `?priority=`) |
| POST | `/tasks` | Create and auto-classify a task |
| GET | `/tasks/<id>` | Get a single task |
| PUT | `/tasks/<id>` | Update title, description, or status |
| DELETE | `/tasks/<id>` | Delete a task |
| GET | `/tasks/summary` | AI-generated priority summary |
 
---
 
## Project structure
 
```
ai-task-api/
├── app.py           # Flask API — routes and request handling
├── classifier.py    # AI task classifier — keyword-based categorization
├── prioritizer.py   # AI prioritizer — urgency scoring and priority labels
├── demo.py          # Demo script showing API in action
├── requirements.txt
└── README.md
```
 
---
 
## Key concepts demonstrated
 
- **REST API design** — clean routes, proper HTTP status codes, JSON responses
- **Modular backend architecture** — classifier, prioritizer, and API fully decoupled
- **AI rule engine** — keyword signal extraction for classification and scoring
- **Cloud-ready structure** — swap in-memory store for PostgreSQL with one change
- **Extensible** — plug in OpenAI or a local LLM for richer classification
---
 
## Tech stack
 
Python · Flask · REST API
 
---
 
## Author
 
Adhiman Jagota — Data Science & Applied Math @ University of Washington Seattle

adhimanj@uw.edu
