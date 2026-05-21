"""
AI Task API — A lightweight backend API powered by AI
Demonstrates: REST API design, AI integration, backend systems, cloud-ready structure
"""

from flask import Flask, request, jsonify
from classifier import TaskClassifier
from prioritizer import TaskPrioritizer
import uuid
from datetime import datetime

app = Flask(__name__)

# In-memory task store (swap for a DB in production)
tasks = {}
classifier = TaskClassifier()
prioritizer = TaskPrioritizer()


def make_task(title: str, description: str = "") -> dict:
    category = classifier.classify(title, description)
    priority = prioritizer.score(title, description, category)
    return {
        "id":          str(uuid.uuid4())[:8],
        "title":       title,
        "description": description,
        "category":    category,
        "priority":    priority["label"],
        "priority_score": priority["score"],
        "status":      "pending",
        "created_at":  datetime.utcnow().isoformat() + "Z",
    }


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "AI Task API",
        "version": "1.0.0",
        "endpoints": [
            "GET  /tasks         — list all tasks",
            "POST /tasks         — create and auto-classify a task",
            "GET  /tasks/<id>    — get a task",
            "PUT  /tasks/<id>    — update status",
            "DELETE /tasks/<id> — delete a task",
            "GET  /tasks/summary — AI-generated priority summary",
        ]
    })


@app.route("/tasks", methods=["GET"])
def list_tasks():
    category = request.args.get("category")
    priority = request.args.get("priority")
    result = list(tasks.values())
    if category:
        result = [t for t in result if t["category"] == category]
    if priority:
        result = [t for t in result if t["priority"] == priority]
    result = sorted(result, key=lambda t: t["priority_score"], reverse=True)
    return jsonify({"count": len(result), "tasks": result})


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"error": "title is required"}), 400
    task = make_task(data["title"], data.get("description", ""))
    tasks[task["id"]] = task
    return jsonify({"message": "Task created", "task": task}), 201


@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    valid_statuses = {"pending", "in_progress", "done"}
    if "status" in data:
        if data["status"] not in valid_statuses:
            return jsonify({"error": f"status must be one of {valid_statuses}"}), 400
        task["status"] = data["status"]
    if "title" in data or "description" in data:
        task["title"]       = data.get("title", task["title"])
        task["description"] = data.get("description", task["description"])
        reclassified        = make_task(task["title"], task["description"])
        task["category"]    = reclassified["category"]
        task["priority"]    = reclassified["priority"]
        task["priority_score"] = reclassified["priority_score"]
    return jsonify({"message": "Task updated", "task": task})


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    del tasks[task_id]
    return jsonify({"message": f"Task {task_id} deleted"})


@app.route("/tasks/summary", methods=["GET"])
def summary():
    if not tasks:
        return jsonify({"message": "No tasks yet."})
    by_priority = {"high": [], "medium": [], "low": []}
    by_category = {}
    for t in tasks.values():
        by_priority[t["priority"]].append(t["title"])
        by_category.setdefault(t["category"], 0)
        by_category[t["category"]] += 1
    return jsonify({
        "total_tasks":    len(tasks),
        "by_priority":    {k: len(v) for k, v in by_priority.items()},
        "by_category":    by_category,
        "top_priority":   by_priority["high"][:3],
        "pending":        sum(1 for t in tasks.values() if t["status"] == "pending"),
        "in_progress":    sum(1 for t in tasks.values() if t["status"] == "in_progress"),
        "done":           sum(1 for t in tasks.values() if t["status"] == "done"),
    })


if __name__ == "__main__":
    print("AI Task API running at http://localhost:5000")
    app.run(debug=True, port=5000)
