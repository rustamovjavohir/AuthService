import datetime

from pydantic import BaseModel, BaseConfig


def convert_datetime_to_realword(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word.capitalize() if index != 0 else word
        for index, word in enumerate(string.split("_"))
    )


class RWModel(BaseModel):
    """
    Base class for models that should be read and written to the database.
    """

    class Config(BaseConfig):
        populate_by_name = True
        json_encoders = {datetime.datetime: convert_datetime_to_realword}
        # alias_generator = convert_field_to_camel_case


class IdMixin(BaseModel):
    """
    Mixin for id field.
    """

    id: int


class DateTimeMixin(BaseModel):
    """
    Mixin for datetime fields.
    """

    created_at: datetime.datetime
    updated_at: datetime.datetime | None = None
