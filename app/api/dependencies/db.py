from typing import Callable

from app.db.database import SessionLocal


def get_db():
    with SessionLocal() as db:
        yield db


def get_service(service) -> Callable:
    return service
