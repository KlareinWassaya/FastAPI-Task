from src.common.exceptions.service_custom_exception import ServiceCustomException
from src.repositories.task import TaskRepository
from src.enums.user import UserRole


class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    def get_all(self, user_id: int):
        return self.task_repo.get_all(user_id)
    
    def get_all_tasks(self, role):
        if role != UserRole.ADMIN.value:
            raise ServiceCustomException("permission denied. Permission only allowed for admins")
        return self.task_repo.get_all_tasks()

    def get_task_by_id(self, task_id: int, user_id: int):
        task = self.task_repo.get_by_id(task_id, user_id)
        if not task:
            raise ServiceCustomException("Task not found")
        return task

    def create_task(self, task_data, user_id: int):
        if self.task_repo.get_by_title(task_data["title"], user_id):
            raise ServiceCustomException("Task title already exists")
        return self.task_repo.create(task_data, user_id)

    def mark_done(self, task_id, user_id):
        if self.get_task_by_id(task_id, user_id):
            return self.task_repo.mark_done(task_id)

    def change_priority(self, new_priority, task_id, user_id):
        if self.get_task_by_id(task_id, user_id):
            return self.task_repo.change_priority(task_id, new_priority)

    def delete_task(self, task_id: int, user_id: int, role: str):
        task = self.get_task_by_id(task_id, user_id)
        return self.task_repo.delete_task(task.id)