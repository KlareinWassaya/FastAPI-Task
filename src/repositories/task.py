from sqlalchemy.orm import Session

from src.models.task import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: int):
        return self.db.query(Task).filter(Task.user_id == user_id).all()
    
    def get_all_tasks(self):
        return self.db.query(Task).all()

    def get_by_id(self, task_id: int, user_id: int):
        return self.db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    def get_by_title(self, title: str, user_id: int):
        return self.db.query(Task).filter(Task.title == title, Task.user_id == user_id).first()

    def create(self, task_data, user_id: int):
        new_task = Task(**task_data, user_id=user_id)
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task
        
    def mark_done(self, task_id: int):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        task.done = True
        self.db.commit()
        self.db.refresh(task)
        return task

    def change_priority(self, task_id: int, new_priority: int):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        task.priority = new_priority
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        self.db.delete(task)
        self.db.commit()
        return True