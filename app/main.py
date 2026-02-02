from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db, engine
from app.models import Base
from app import crud, schemas

app = FastAPI(title="Task Manager Professional")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/tasks", response_model=list[schemas.TaskResponse])
async def read_tasks(completed: Optional[bool] = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_tasks(db, completed=completed)

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db, task)

@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    updated_task = await crud.update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")