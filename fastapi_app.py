from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional

app = FastAPI()

# In-memory task store
tasks: List["Task"] = []


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    assignee: Optional[EmailStr] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee: Optional[EmailStr] = None


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    tasks.append(task)
    return task


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: TaskUpdate):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = updated_task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    # Re-assigning the global 'tasks' list breaks state management for tests
    # that import the list. Instead, we modify the list in-place.
    tasks[:] = [t for t in tasks if t.id != task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
