from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


# Получить все задачи
async def get_tasks(db: AsyncSession, completed: bool = None):
    query = select(Task)
    if completed is not None:
        query = query.where(Task.completed == completed)
    result = await db.execute(query)
    return result.scalars().all()


# Получить одну по ID
async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


# Создать
async def create_task(db: AsyncSession, task_data: TaskCreate):
    new_task = Task(**task_data.dict())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


# Обновить
async def update_task(db: AsyncSession, task_id: int, task_data: TaskUpdate):
    task = await get_task(db, task_id)
    if not task:
        return None

    # Обновляем только те поля, которые прислал пользователь
    update_data = task_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task


# Удалить
async def delete_task(db: AsyncSession, task_id: int):
    task = await get_task(db, task_id)
    if task:
        await db.delete(task)
        await db.commit()
        return True
    return False