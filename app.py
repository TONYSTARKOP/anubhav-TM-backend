from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

TASK_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_tasks(data):
    with open(TASK_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/tasks", methods=["POST"])
def post_tasks():
    data = request.get_json()  # Parse the incoming JSON
    if not data:
        return jsonify({"error": "Invalid JSON format."}), 400

    if "date" not in data or "tasks" not in data:
        return jsonify({"error": "'date' and 'tasks' are required."}), 400

    tasks = load_tasks()
    tasks[data["date"]] = [{"name": t["name"], "time": t["time"], "completed": False} for t in data["tasks"]]
    save_tasks(tasks)
    return jsonify({"message": "Tasks added successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
