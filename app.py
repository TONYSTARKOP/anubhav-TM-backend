from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)

# Allow all domains for simplicity (replace with your frontend URL in production for security)
CORS(app, origins=["https://anubhav-tm-frontend-ppvg.vercel.app"])

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

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    today = datetime.now().strftime("%Y-%m-%d")
    return jsonify(tasks.get(today, []))

@app.route("/tasks", methods=["POST"])
def post_tasks():
    data = request.json
    tasks = load_tasks()
    tasks[data["date"]] = [{"name": t["name"], "time": t["time"], "completed": False} for t in data["tasks"]]
    save_tasks(tasks)
    return jsonify({"message": "Tasks added successfully"}), 200

@app.route("/tasks/complete", methods=["POST"])
def complete_task():
    data = request.json
    tasks = load_tasks()
    date_tasks = tasks.get(data["date"], [])
    for task in date_tasks:
        if task["name"] == data["name"]:
            task["completed"] = True
            break
    save_tasks(tasks)
    return jsonify({"message": "Task marked as completed"}), 200

@app.route("/report", methods=["GET"])
def daily_report():
    tasks = load_tasks()
    today = datetime.now().strftime("%Y-%m-%d")
    incomplete_tasks = [task for task in tasks.get(today, []) if not task["completed"]]
    return jsonify({"incomplete": incomplete_tasks})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
