import datetime
import re
import enum

from . import language
from .language import Language


DATE_BREAK = Language.DATE
DUR_BREAK = Language.DURATION
WORD_BREAK = ['and', 'or']


class Parsed(enum.Enum):
    
    TIMEDELTA = 0
    DATETIME = 1


def parse(tokens, dates, deltas):
    collection = []
    offset = 0
    start = None
    end = None
    breaking = None

    for index, (kind, value) in enumerate(tokens):
        collection.append((kind, value))

        # Track the last time one of kinds from the break list was seen.
        # Stop tracking if it is a previously parsed kind for this group.
        # This prevents different groups from merging.
        if (breaking is not None and breaking in kind
        and not any(k == kind for k, v in collection[:-1])
        and kind != Language.WORD):
            end = index + 1 - offset

        # If nothing from the breaklist was seen and it was not a word,
        # this means its a different kind of group.
        elif (breaking is not None and
             (kind != Language.WORD or any(w in value for w in WORD_BREAK))):
            if start != 0:
                yield from collection[:start - 1]
            yield from _parse_collection(collection[start:end], breaking,
                                         dates, deltas)

            if any(w in value for w in WORD_BREAK):
                yield from collection[end:]
            else:
                yield from collection[end:-1]

            collection = [(kind, value)]
            offset = index
            start = None
            end = None
            breaking = None
        elif breaking is None and kind == Language.WORD:
            yield (kind, value)

        # Start looking for DATE_BREAK kinds and group them together,
        if breaking is None and DATE_BREAK in kind:
            breaking = DATE_BREAK
            if start is None:
                start = index - offset
                end = start + 1

        # Start looking for DUR_BREAK kinds and group them together,
        if breaking is None and DUR_BREAK in kind:
            breaking = DUR_BREAK
            if start is None:
                start = index - offset
                end = start + 1

    if breaking is not None and collection != []:
        if start != 0:
            yield from collection[:start - 1]
        yield from _parse_collection(collection[start:end], breaking,
                                     dates, deltas)
        yield from collection[end:]


def _parse_collection(collection, breaking, dates, deltas):
    items = strip(collection, Language.WORD)

    if breaking == DATE_BREAK:
        ykind = Parsed.DATETIME
        base = dates()
    else:
        base = deltas()
        ykind = Parsed.TIMEDELTA


    yield (ykind, _parse(items, base))


def strip(tokens, *ignore):
    for (kind, values) in tokens:
        if kind not in ignore:
            yield (kind, values)


def _parse(tokens, base):
    parsers = PARSERS

    for (kind, values) in tokens:
        parser = parsers.get(kind, None)

        if parser is not None:
            for value in values:
                base = parser(base, value)
    return base


def _parse_time(date, value):
    hr = '0'
    mn = '0'
    sc = '0'

    am = value.endswith('am')
    pm = value.endswith('pm')

    t = value.rstrip('amp')

    if ':' in t:
        hr, mn = t.split(':', 1)
    else:
        hr = int(t)

    if '.' in mn:
        mn, sc = mn.split('.', 1)

    if pm:
        hr = int(hr) + 12
    return date.replace(hour=int(hr), minute=int(mn), second=int(sc))


def _parse_date(date, value):
    day = int(value.rstrip('stndrdth'))
    return date.replace(day=day)


def _parse_day_name(date, value):
    weekday = language.DAYS.index(value.lower())
    difference = weekday - date.weekday()
    return date.replace(day=date.day + difference)


def _parse_day(date, value):
    if value.lower().endswith('ago'):
        duration = _parse_days(datetime.timedelta(), value)
        return date - duration
    return date

def _parse_month(date, value):
    month = language.MONTHS.index(value.lower())
    return date.replace(month=month + 1)


def _parse_year(date, value):
    return date.replace(year=int(value))

def _parse_second(date, value):
    duration = _parse_seconds(datetime.timedelta(), value)
    if value.lower().endswith('ago'):
        return date - duration
    return date + duration


def _parse_minute(date, value):
    duration = _parse_minutes(datetime.timedelta(), value)
    if value.lower().endswith('ago'):
        return date - duration
    return date


def _parse_hour(date, value):
    duration = _parse_hours(datetime.timedelta(), value)
    if value.lower().endswith('ago'):
        return date - duration
    return date


def _parse_relative(date, value):
    addition = language.RELATIVE.get(value.lower(), 0)
    return date.replace(day=date.day + addition)


def _parse_prefix(date, value):
    pref, day = value.split(' ', 1)

    if (pref.lower() in ['next', 'last']
    and day.lower() in language.DAYS + ['week']):
        days = (7 if pref.lower() == 'next' else -7)
        date = date + datetime.timedelta(days=days)

    if day.lower() == 'fortnite':
        days = (14 if pref.lower() == 'next' else -14)
        date = date + datetime.timedelta(days=days)

    if day.lower() == 'month':
        months = (1 if pref.lower() == 'next' else -1)
        date = date.replace(month=date.month + months)

    if day.lower() == 'year':
        years = (1 if pref.lower() == 'next' else -1)
        date = date.replace(year=date.year + years)

    if day.lower() in language.DAYS:
        date = _parse_day_name(date, day)
    return date


def _parse_hours(duration, value):
    number, *suffix = value.split(' ', 1)
    hour = int(number.rstrip('hours'))
    return duration + duration.__class__(hours=hour)


def _parse_minutes(duration, value):
    number, *suffix = value.split(' ', 1)
    minute = int(number.rstrip('minutes'))
    return duration + duration.__class__(minutes=minute)


def _parse_seconds(duration, value):
    number, *suffix = value.split(' ', 1)
    second = int(number.rstrip('second'))
    return duration + duration.__class__(seconds=second)


def _parse_days(duration, value):
    number, suffix = value.split(' ', 1)
    days = int(number.rstrip('days'))
    return duration + duration.__class__(days=days)


def _parse_weeks(duration, value):
    number, suffix = value.split(' ', 1)
    days = int(number.rstrip('weeks')) * 7
    return duration + duration.__class__(days=days)


def _parse_years(duration, value):
    number, suffix = value.split(' ', 1)
    days = int(number.rstrip('years')) * 365
    return duration


PARSERS = {
    Language.PREFIX | Language.DAY | Language.DATE: _parse_date,
    Language.DAY | Language.DATE | Language.WEEK: _parse_day_name,
    Language.MONTH | Language.DATE: _parse_month,

    Language.TIME | Language.DATE: _parse_time,
    Language.DAY | Language.DATE: _parse_day,
    Language.YEAR | Language.DATE: _parse_year,
    Language.PREFIX | Language.DATE: _parse_prefix,
    Language.HOUR | Language.DATE: _parse_hour,
    Language.MINUTE | Language.DATE: _parse_minute,
    Language.SECOND | Language.DATE: _parse_second,
    Language.RELATIVE | Language.DATE: _parse_relative,

    Language.HOUR | Language.DURATION: _parse_hours,
    Language.MINUTE | Language.DURATION: _parse_minutes,
    Language.SECOND | Language.DURATION: _parse_seconds,
    Language.DAY | Language.DURATION: _parse_days,
    Language.WEEK | Language.DURATION: _parse_weeks,
}
