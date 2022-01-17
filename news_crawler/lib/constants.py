from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=+9), "JST")
YESTERDAY = (datetime.now(tz=JST) - timedelta(days=1)).date()
