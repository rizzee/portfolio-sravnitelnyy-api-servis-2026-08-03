from flask import Flask, jsonify, request, abort
from pydantic import BaseModel, EmailStr, ValidationError
from typing import List, Optional

app = Flask(__name__)

# In-memory task store
tasks = []


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    assignee: Optional[EmailStr] = None


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([task.dict() for task in tasks])


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int):
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        abort(404)
    return jsonify(task.dict())


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_id = max([task.id for task in tasks] or [0]) + 1
    data.pop('id', None) # Prevent TypeError by removing client-sent id
    try:
        task = Task(id=new_id, **data)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    tasks.append(task)
    return jsonify(task.dict()), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int):
    data = request.json
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        abort(404)
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.assignee = data.get('assignee', task.assignee)
    return jsonify(task.dict())


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t.id != task_id]
    return '', 204
