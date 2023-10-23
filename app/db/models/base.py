from sqlalchemy import (Column, BigInteger, Integer, String, Boolean, ForeignKey, DateTime)
from sqlalchemy.sql import func
from app.db.database import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(
        BigInteger,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
    )

    def __str__(self):
        return f"{self.__class__.__name__}({self.id}) - {self.created_at}"
