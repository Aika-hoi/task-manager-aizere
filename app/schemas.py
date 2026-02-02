from pydantic import BaseModel
from typing import Optional

# Что нам нужно для создания задачи
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

# Что мы можем обновить в задаче (все поля необязательные)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Что мы отдаем пользователю в ответ
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        from_attributes = True