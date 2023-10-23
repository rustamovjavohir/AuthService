import sqlalchemy_utils
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

SQLALCHEMY_DATABASE_URL = DATABASE_URL

# check_same_thread  this is only for sqlite
engine = create_engine(
    str(SQLALCHEMY_DATABASE_URL)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata


def render_item(type_, obj, autogen_context):
    """Apply custom rendering for selected items."""

    if type_ == "type" and obj.__class__.__module__.startswith("sqlalchemy_utils."):
        autogen_context.imports.add(f"import {obj.__class__.__module__}")
        if hasattr(obj, "choices"):
            return f"{obj.__class__.__module__}.{obj.__class__.__name__}(choices={obj.choices})"
        else:
            return f"{obj.__class__.__module__}.{obj.__class__.__name__}()"

    # default rendering for other objects
    return False
