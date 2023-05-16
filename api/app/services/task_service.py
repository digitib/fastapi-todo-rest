from sqlalchemy.orm import Session

from app.enums import TaskVisibilityEnum
from app.models import Task, User
from app.schemas.task import TaskCreate, TaskUpdate

from .base_service import BaseService
from .exceptions import OwnerAccessViolationException


class TaskService(BaseService[Task]):
    def get_for_user(self, db: Session, id: int, user_owner: User) -> Task | None:
        """
        Get a task by id. Check if the user is an owner of the task.
        """
        task = self._get(db, id)
        if task is None:
            return None
        self._check_is_owner(db, task, user_owner)
        return task

    def get_for_user_or_exception(self, db: Session, id: int, user_owner: User) -> Task:
        """
        Get a task by id. Raise exception if not found. Check if the user is an
        owner of the task.
        """
        task = self._get_or_exception(db, id)
        self._check_is_owner(db, task, user_owner)
        return task

    def list_by_user(
        self,
        db: Session,
        user: User,
        *,
        visibility: TaskVisibilityEnum | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        query = db.query(Task).filter(Task.user_id == user.id)
        if visibility is not None:
            query = query.filter(Task.visibility == visibility)
        return query.offset(offset).limit(limit).all()

    def create_for_user(
        self, db: Session, create_api_model: TaskCreate, user: User
    ) -> Task:
        """
        Create a new task with a given user as owner.
        """
        data_to_create_prepared = dict(
            **create_api_model.dict(),
            user_id=user.id,
        )
        return self._create(db, data_to_create_prepared)

    def update(
        self,
        db: Session,
        db_model: Task,
        update_api_model: TaskUpdate,
    ) -> None:
        data_to_update_prepared = update_api_model.dict()
        self._update(db, db_model, data_to_update_prepared)

    def delete(self, db: Session, db_model: Task) -> None:
        self._delete(db, db_model)

    def _check_is_owner(self, db: Session, db_model: Task, user: User) -> None:
        if db_model.user_id != user.id:
            raise OwnerAccessViolationException(
                "Access forbidden as the user is not an owner"
            )


task_service = TaskService(Task)