"""Shared fixtures for the serializer tests."""

from datetime import datetime, timedelta, tzinfo


class FixedOffset(tzinfo):
    """Represent UTC+01:00 on all supported Python versions."""

    def utcoffset(self, value):
        # type: (datetime | None) -> timedelta
        """Return the fixed offset from UTC."""
        return timedelta(hours=1)
