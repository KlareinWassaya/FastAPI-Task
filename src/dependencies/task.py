from fastapi import Depends
from sqlalchemy.orm import Session

from src.common.db.connection import get_db
from src.repositories.task import TaskRepository
from src.services.task import TaskService


def get_task_service(db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    return TaskService(repo)
