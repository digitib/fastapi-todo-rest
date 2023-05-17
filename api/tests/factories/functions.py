from typing import TypeVar

from faker import Faker
from sqlalchemy.orm import Session

from app.models import BaseDBModel, Task, User
from tests.common import get_db_model_or_exception

from . import task

DBModelType = TypeVar("DBModelType", bound=BaseDBModel)


def persist(db: Session, db_model: DBModelType) -> None:
    """
    Persist a DB model to the database.
    """
    db.add(db_model)
    db.commit()
    db.refresh(db_model)


def make_task_persisted(
    db: Session, faker: Faker, *, user_owner_username: str, subject: str
) -> Task:
    user_owner = get_db_model_or_exception(db, User, username=user_owner_username)
    target_task = task.make(
        faker,
        user=user_owner,
        subject=subject,
    )
    persist(db, target_task)
    return target_task