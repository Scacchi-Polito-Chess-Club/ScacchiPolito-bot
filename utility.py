from datetime import datetime, timedelta


def toTimestamp(date):
    t = date.timestamp()
    return int(t)*1000


def nextSunday():
    now = datetime.now()
    year, week, weekday = now.isocalendar()
    if weekday == 7 and now.hour >= 15:
        week += 1
    nextSunday = datetime.fromisocalendar(year, week, 7)
    return nextSunday + timedelta(hours=19, minutes=15)