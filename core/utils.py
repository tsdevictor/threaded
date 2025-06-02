from datetime import datetime, timezone


def get_relative_time(created_utc):
    now = datetime.now(timezone.utc)
    dt = datetime.fromtimestamp(created_utc, tz=timezone.utc)
    diff = (now - dt).total_seconds()

    if diff < 60:
        return "just now"
    elif diff < 3600:
        return f"{int(diff // 60)} minutes ago"
    elif diff < 86400:
        return f"{int(diff // 3600)} hours ago"
    elif diff < 604800:
        return f"{int(diff // 86400)} days ago"
    else:
        return dt.strftime('%b %d, %Y')