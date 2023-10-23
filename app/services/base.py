from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.db import get_db


class BaseService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
