import json
import os
import re
import string

import songsheet

test_path = os.path.dirname(os.path.abspath(__file__))


def test_compose():
    clean_str = songsheet.compose(
        lambda s: s.strip(), lambda s: s.replace('-', ''))
    assert clean_str('   foo-bar  ') == 'foobar'


def test_valid_chords():
    assert len(songsheet.valid_chords) == 85
    assert(songsheet.valid_chords[:15]) == ['a', 'a#', 'am', 'a#7', 'a#m7', 'a#sus',
                                            'a♭', 'a♭m', 'a♭7', 'a♭m7', 'a♭sus', 'am', 'a7', 'am7', 'asus']


def test_no_wrong_incidentals():
    assert 'b#' not in songsheet.valid_chords
    assert 'c♭' not in songsheet.valid_chords
    assert 'e#' not in songsheet.valid_chords
    assert 'f♭' not in songsheet.valid_chords


def test_strip_spaces_each_line():
    assert songsheet.strip_spaces_each_line('foo \n bar') == 'foo\nbar'


def test_normalize_line_breaks():
    assert songsheet.normalize_line_breaks(
        'foo\rbar\nbat') == 'foo\nbar\nbat'


def test_clean():
    assert songsheet.clean('  foo\n \n \rbar bat ') == 'foo\nbar bat'


def test_is_chord_line():
    assert songsheet.is_chord_line(['GM', ' ', 'c#']) == True
    assert songsheet.is_chord_line(['aa', 'b']) == False
    assert songsheet.is_chord_line(['foo']) == False
    assert songsheet.is_chord_line(['GM', ' ', ' ', ' ', 'A']) == True


def test_serialize():
    content = '''
GM  A
foo bar
C#
bat
'''
    assert songsheet.serialize(content) == (
        ('GM', ' ', ' ', 'A'), ('f', 'o', 'o', ' ', 'b', 'a', 'r'), ('C#',), ('b', 'a', 't'))


def test_to_json():
    content = '''
G  A
foo bar
B
bat  '''

    assert json.loads(songsheet.to_json(content)) == [['G', ' ', ' ', 'A'], [
        'f', 'o', 'o', ' ', 'b', 'a', 'r'], ['B'], ['b', 'a', 't']]


def test_to_json_indent():
    content = '''
G  A
foo bar
B
bat  '''
    json_str = songsheet.to_json(content, 2)
    assert re.match(r'\[\n\s{2}\[', json_str)


def test_compact_chords():
    assert songsheet.compact_chords(['g', '#', 'm', '7', ' ', 'a7']) == [
        'g#m7', ' ', 'a7']
    assert songsheet.compact_chords(['G', 'M', ' ', ' ', 'A']) == [
        'GM', ' ', ' ', 'A']
    assert songsheet.compact_chords(['C', '#']) == ['C#']


def test_to_str():
    assert songsheet.to_str(
        (('F#', ' ', ' '), ('f', 'o', 'o'))) == 'F#  \nfoo'
