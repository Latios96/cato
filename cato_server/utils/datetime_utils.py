import datetime


def aware_now_in_utc():
    return datetime.datetime.now(datetime.timezone.utc)
