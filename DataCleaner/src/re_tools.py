import re


def drop_year(x):
    return re.sub(r"[\d]{4}", "", x)


def drop_day(x):
    return re.sub(r"[\d]{1,2}[a-z]{2}", "", x)


def drop_week(x):
    return re.sub(r"[\d]{1,2}-[a-z]{4}", "", x)


def drop_day_week_and_year(x):
    x = drop_day(x)
    x = drop_week(x)
    x = drop_year(x)
    return x
