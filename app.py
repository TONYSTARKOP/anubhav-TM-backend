from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# File to store tasks
TASK_FILE = "tasks.json"

# Load tasks from the file
def load_tasks():
    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save tasks to the file
def save_tasks(data):
    with open(TASK_FILE, "w") as file:
        json.dump(data, file, indent=4)

# API to get today's tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    today = datetime.now().strftime("%Y-%m-%d")
    return jsonify(tasks.get(today, []))

# API to submit tasks for the next day
@app.route("/tasks", methods=["POST"])
def post_tasks():
    data = request.json  # {"date": "YYYY-MM-DD", "tasks": [...]}
    tasks = load_tasks()
    tasks[data["date"]] = [{"name": t["name"], "time": t["time"], "completed": False} for t in data["tasks"]]
    save_tasks(tasks)
    return jsonify({"message": "Tasks added successfully"}), 200

# API to mark a task as completed
@app.route("/tasks/complete", methods=["POST"])
def complete_task():
    data = request.json  # {"date": "YYYY-MM-DD", "name": "Task Name"}
    tasks = load_tasks()
    date_tasks = tasks.get(data["date"], [])
    for task in date_tasks:
        if task["name"] == data["name"]:
            task["completed"] = True
            break
    save_tasks(tasks)
    return jsonify({"message": "Task marked as completed"}), 200

# API to get the daily report
@app.route("/report", methods=["GET"])
def daily_report():
    tasks = load_tasks()
    today = datetime.now().strftime("%Y-%m-%d")
    incomplete_tasks = [task for task in tasks.get(today, []) if not task["completed"]]
    return jsonify({"incomplete": incomplete_tasks})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

