import enum
import calendar

from . import lexer


DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
MONTHS = [m.lower() for m in calendar.month_name[1:]]
WORD_NUMS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']

PREFIXES = ['next', 'last', 'this']

RELATIVE = {
    'today': 0,
    'tomorrow': 1,
    'overmorrow': 2,
    'yesterday': -1
}


class Language(enum.IntFlag):

    WORD = 0

    SECOND = 1
    MINUTE = 2
    HOUR = 4

    DAY = 8
    WEEK = 16
    MONTH = 32
    YEAR = 64

    DURATION = 128
    DATE = 256
    PREFIX = 512
    TIME = 1024

    RELATIVE = 2048


# Duration modifiers.
MODIFIERS = {
    'second': Language.SECOND,
    'minute': Language.MINUTE,
    'hour': Language.HOUR,
    'day': Language.DAY,
    'week': Language.WEEK,
    'month': Language.MONTH,
    'year': Language.YEAR,
}

MOD_ALIAS = {
    'sec': MODIFIERS['second'],
    's': MODIFIERS['second'],
    'min': MODIFIERS['minute'],
    'm': MODIFIERS['minute'],
    'fortnite': MODIFIERS['week'],
}

MODIFIERS.update(MOD_ALIAS)


def lex(text, lexfunc=None):
    '''Lex some text and yield token pairs.
    You can specify a custom starting point for the lexer via the lexer param.
    It assumes lexer is a generator that yields Language enum values.
    '''
    lexfunc = lexfunc or _lex
    lex = lexer.Lexer(text) 

    for kind in lexfunc(lex):
        if lex.start == lex.cursor:
            lex.cursor += 1

        value = lex.slice
        if kind == Language.WORD and value.lower() in DAYS:
            yield (Language.DAY | Language.DATE | Language.WEEK, value)
        elif kind == Language.WORD and value.lower() in MONTHS:
            yield (Language.MONTH | Language.DATE, value)
        elif kind == Language.WORD and value.lower() in RELATIVE:
            yield (Language.RELATIVE | Language.DATE, value)
        else:
            yield (kind, value)

        lex.move(0, update=True)

        if lex.eof:
            break


def group(tokens):
    prev = None
    values = []

    for (kind, value) in tokens:
        if prev is None:
            prev = kind

        if kind != prev:
            yield (prev, values)
            prev = None
            values = []

        values.append(value)
        prev = kind

    if len(values):
        yield (prev, values)


def _lex(lex):
    for char in lex.step:

        if lex.slice.lower() in PREFIXES:
            yield from lex_prefix(lex)

        if char.isnumeric():
            yield from lex_numeric(lex)

        if not char.isalnum():
            lex.consumewhile(lambda c: c.isalnum())
            yield Language.WORD
            lex.move(-1)

    yield Language.WORD


def lex_prefix(lex):
    possible = ['week', 'month', 'year', 'fortnite']
    lex.consume(' ', False)
    for pref in possible:
        if lex.next(len(pref)) == pref:
            lex.move(len(pref))
            yield Language.PREFIX | Language.DATE
            break
    

def lex_numeric(lex):
    for char in lex.step:

        # Uh oh its actually a date.
        if lex.next(2) in ['st', 'nd', 'th']:
            lex.move(2)
            yield Language.PREFIX | Language.DAY | Language.DATE
            break

        if any(m in lex.next(len(m) + 1).strip(' ') for m in MODIFIERS.keys()):
            yield from lex_duration(lex)
        
        # It's a 12 hour time.
        if lex.next(2) in ['am', 'pm']:
            lex.move(2)
            yield Language.TIME | Language.DATE
            break

        if not char.isnumeric() and char not in [':', '.']:
            break

    # Check if it was a 24 hour time or a year,
    length = abs(lex.cursor - lex.start)
    if length == 4 and lex.slice.isnumeric():
       yield Language.YEAR | Language.DATE

    elif ':' in lex.slice:
        # 24 hour time
        yield Language.TIME | Language.DATE

    # Backup required.
    lex.move(-1)


def lex_duration(lex):
    char = lex.char
    if char == ' ':
        lex.move(1)

    for m in sorted(MODIFIERS.keys(), key=len, reverse=True):
        if (len(m) == 1 and m == lex.next(1)
        or len(m) != 1 and m == lex.next(len(m))):
            lex.move(len(m))

            if lex.next(1) == 's':
                lex.move(1)

            kind = MODIFIERS[m]

            if lex.next(4).lower() == ' ago':
                lex.move(4)
                yield kind | Language.DATE
            else:
                yield kind | Language.DURATION
