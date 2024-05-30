"""
📌Необходимо создать API для управления списком задач. Каждая задача должна
содержать заголовок и описание. Для каждой задачи должна быть возможность
указать статус (выполнена/не выполнена).
📌API должен содержать следующие конечные точки:
○GET /tasks - возвращает список всех задач.
○GET /tasks/{id} - возвращает задачу с указанным идентификатором.
○POST /tasks - добавляет новую задачу.
○PUT /tasks/{id} - обновляет задачу с указанным идентификатором.
○DELETE /tasks/{id} - удаляет задачу с указанным идентификатором.
Для каждой конечной точки необходимо проводить валидацию данных запроса и
ответа. Для этого использовать библиотеку Pydantic.
"""

import logging
from typing import List

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from lesson_5.fastapi_hw5.ORM_models import TaskBase, get_db, Base, engine
from lesson_5.fastapi_hw5.pydentic_models import Task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/tasks/", response_model=List[Task])
async def get_tasks(db: Session = Depends(get_db)):
    """
    метод получения всех задач
    """
    logger.info('>> GET a request to receive all the tasks has been sent')
    all_tasks = db.query(TaskBase).all()
    return [Task.from_orm(t) for t in all_tasks]


@app.post("/tasks/", response_model=Task)
async def create_task(new_task: Task, db: Session = Depends(get_db)):
    """
    метод добавления задачи
    """
    logger.info('>> POST request to add a task has been sent')

    new_task = TaskBase(
        title=new_task.title,
        description=new_task.description,
        completed=False
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return Task.from_orm(new_task)


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    метод получения задачи по ID
    """
    logger.info('>> GET request to search a task by ID has been sent')
    task = db.query(TaskBase).filter(TaskBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task.from_orm(task)


@app.put("/tasks/{task_id}", response_model=Task)
async def change_task(task_id: int, edited_task: Task, db: Session = Depends(get_db)):
    """
    метод изменения задачи по ID
    """
    logger.info('>> PUT request to change a task by ID has been sent')
    task = db.query(TaskBase).filter(TaskBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = edited_task.title
    task.description = edited_task.description
    task.completed = edited_task.completed
    db.commit()
    db.refresh(task)
    return Task.from_orm(task)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    метод удаления задачи по ID
    """
    logger.info(f'>> DELETE request to remove task ID {task_id} has been sent')
    task = db.query(TaskBase).filter(TaskBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task with ID {task_id} has been deleted"}
