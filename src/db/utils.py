from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.types import DateTime, TypeDecorator


class TZDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: Optional[datetime], dialect):
        if value is not None:
            if not value.tzinfo:
                raise TypeError("tzinfo is required")
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value: Optional[datetime], dialect):
        if value is not None:
            value = value.replace(tzinfo=timezone.utc)
        return value
