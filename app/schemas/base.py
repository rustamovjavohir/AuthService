from datetime import datetime

from app.db.domain.base import RWModel


class RWSchema(RWModel):
    class Config(RWModel.Config):
        # orm_mode = True
        from_attributes = True

