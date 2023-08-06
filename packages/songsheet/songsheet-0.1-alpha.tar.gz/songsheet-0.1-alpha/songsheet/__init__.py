"""
A python module for working with songsheets. Songsheets are simple sheets
showing a song's lyrics, chords, progression patterns and chord diagrams.
"""

import functools
import json
import os
import re
import string
from typing import Any, Callable, List, Pattern, Tuple


valid_chords: List[str] = []
"""list: A list of common chords"""

flat_char = '\u266D'
for chord in string.ascii_lowercase[:7]:
    valid_chords.append(chord)
    if chord not in ['b', 'e']:
        valid_chords.append(f'{chord}#')
        valid_chords.append(f'{chord}m')
        valid_chords.append(f'{chord}#7')
        valid_chords.append(f'{chord}#m7')
        valid_chords.append(f'{chord}#sus')
    if chord not in ['c', 'f']:
        valid_chords.append(f'{chord}{flat_char}')
        valid_chords.append(f'{chord}{flat_char}m')
        valid_chords.append(f'{chord}{flat_char}7')
        valid_chords.append(f'{chord}{flat_char}m7')
        valid_chords.append(f'{chord}{flat_char}sus')
    valid_chords.append(f'{chord}m')
    valid_chords.append(f'{chord}7')
    valid_chords.append(f'{chord}m7')
    valid_chords.append(f'{chord}sus')

valid_chords_re: Pattern = re.compile(
    '(' + '|'.join([f'\\b{chord}\\b' for chord in valid_chords]) + ')', re.IGNORECASE)
"""A case-insensitive regular expression matching any valid chord."""


def compose(*funcs: Any) -> Callable:
    """ Composes a list of functions into a single composite func.

    Args:
        funcs: a list of functions

    Returns:
        A function composed of the passed-in functions.
    """
    return functools.reduce(lambda f, g: lambda x: f(g(x)), funcs)


def normalize_line_breaks(s: str) -> str:
    """Returns a string with line breaks replaced with
    the OS appropriate line break.

    Args:
        s: A source string.

    Returns:
        A string with line breaks normalized.
    """
    return re.sub(r'[\n\r]+', os.linesep, s)


strip_spaces_each_line = compose(lambda s: re.sub(f'\\s+{os.linesep}', os.linesep, s),
                                 lambda s: re.sub(f'{os.linesep}\\s', os.linesep, s))
"""Strips spaces before and after each new line.

    Args:
        x (str): An input string.

    Returns:
        str: A string with spaces stripped before and after each new-line.
"""


def clean(s: str) -> str:
    """Cleans an input songsheet in preparation for parsing. A
    composition of the following functions:

    * strips spaces before and after each line
    * normalizes line breaks.
    * Strips leading and trailing spaces.

    Args:
        x: The input string.

    Returns:
        The cleaned string.
"""
    return compose(lambda s: s.strip(), normalize_line_breaks,
                   strip_spaces_each_line)(s)


def is_chord_line(chord_line: List[str]) -> bool:
    """
    Determines whether an array of characters can be considered a line
    of valid chords.

    Args:
        chord_line: A list of characters.


    Returns:
        `True` if all contigious characters are chords.

    Example:
        >>> songsheet.is_chord_line(['a', 'B', ' ', 'g#m']) 
        True

        >>> songsheet.is_chord_line(['a', 'z', ' ', 'g#m']) 
        False

    """
    return all([valid_chords_re.search(chord) for chord in chord_line if chord != ' '])


def compact_chords(line: List[str]) -> List[str]:
    """Compacts a list of letters such that a multi letter chord
    is one element in the list.

    Args:
        line: A list of characters.

    Returns:
        A list of compacted characters.

    Example:
        >>> songsheet.compact_chords(['g', 'm', ' ', 'B']
        ['gm', ' ', 'B']
    """
    ret = []
    el = ''
    for i, char in enumerate(line):
        if i == len(line) - 1:
            el += char
            ret.append(el)
        elif char == ' ':
            ret.append(el)
            ret.append(' ')
            el = ''
        else:
            el += char

    # Hack, why is there an extra empty string.
    return [char for char in ret if char != '']


def serialize(songsheet_str: str):
    """
    Serializes a songsheet string into a tuple of tuples.

    Args:
        songsheet_str: A string representing a songsheet.

    Returns:
        A tuple of tuples. Each tuple is a line of chords followed by a line of lyrics.

    Example:

        >>> songsheet.serialize('am   C   \\nfoo bar')
        ('Am', ' ', ' ', 'C ', ' ', ' ', ' '),
        ('f', 'o', 'o', ' ', 'b', 'a' 'r'))
    """
    cleaned_song_str = clean(songsheet_str)
    lines = []
    split_str = list(cleaned_song_str)
    for (i, letter) in enumerate(split_str):
        if i == 0:
            line_list: List[str] = []
            lines.append(line_list)
        if letter == '\n':
            line_list = []
            lines.append(line_list)
        else:
            line_list.append(letter)
    data = tuple([tuple(line) for line in lines])

    # TODO make this into function.
    ret = []
    for line in lines:
        compacted = compact_chords(line)
        if is_chord_line(compacted):
            ret.append(compacted)
        else:
            ret.append(line)
    #print( tuple([tuple(line) for line in ret]))
    return tuple([tuple(line) for line in ret])


def to_json(s: str, indent: int = 0) -> str:
    """Returns a json string given a songsheet string.

    Args:
        s: A songsheet string.
        indent: How many spaces to indent (prettify). Defaults to None.

    Returns:
        A string of json
    """
    # Curry json.dumps to freeze the indent parameter, leaving a function
    # that only takes a string. Then compose it with serialize.
    indent_dumps = functools.partial(json.dumps, indent=indent)
    serialize_and_dumps = compose(lambda data: indent_dumps(
        data), lambda s: serialize(s))

    return serialize_and_dumps(s)


def to_str(lines: List[List[str]]) -> str:
    """Converts a parsed songsheet back into a string.

    Args:
        lines: A list of parsed songsheet lines

    Returns:
        A songsheet string.
    """
    ret = ''
    for i, line in enumerate(lines):
        ret += ''.join(line)
        if i != len(lines) - 1:
            ret += '\n'
    return ret
