import datetime


def aware_now_in_utc():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
