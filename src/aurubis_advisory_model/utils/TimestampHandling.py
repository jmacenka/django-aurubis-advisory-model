import pytz
from datetime import datetime, timedelta

from config import (
    TIMEZONE,
)

timezone = pytz.timezone(TIMEZONE)

def tz_aware_timestamp(timestamp: datetime):
    """
    Make a timestamp timezone aware.
    """
    # If the timestamp is naive, assume it is in the timezone of the OSI PI system
    if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
        tz_aware_ts = timezone.localize(timestamp)
    return tz_aware_ts