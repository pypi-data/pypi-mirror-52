# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from itertools import chain

if sys.version_info >= (3, 5):
    from functools import reduce

RESET = '\x1b[0m'


class StyledText(object):
    def __init__(self, text, style=None):
        if isinstance(text, StyledText):
            self.text = text.text
        elif isinstance(text, StyledGroup):
            self.text = text.naked
        else:
            self.text = str(text)
        self.style = style

    def _repr(self, text):
        return ''.join((self.style, text, RESET)) if self.style else text

    def __repr__(self):
        return self._repr(self.text)

    def __len__(self):
        return len(self.text)

    def __getitem__(self, item):
        if isinstance(item, slice):
            raise NotImplemented()

        return self._repr(self.text[item])

    def __add__(self, other):
        if not isinstance(other, (StyledText, StyledGroup)):
            other = StyledText(other)
        return StyledGroup(self, other)

    def __radd__(self, other):
        return StyledGroup(StyledText(other), self)


class StyledGroup(object):
    def __init__(self, styled1, styled2):
        self.data = [(s, n) ]
        if text:
            if isinstance(text, StyledText):
                text = ''.join(x for x, _ in text.data)
            self.data += [(str(text), style)]
        self.indices = reduce(
            lambda acum, (text, _): acum + [acum[-1] + len(text)], self.data, [0]
        )

    @property
    def naked(self):
        return

    def __repr__(self):
        return ''.join(chain.from_iterable(
            (style, text, RESET) if style else (text,) for text, style in self.data
        ))

    def __len__(self):
        return sum(len(text) for text, _ in self.data)

    def __getitem__(self, item):
        for i, (c, s) in enumerate((c, style) for text, style in self.data for c in text):
            if i == item:
                return ''.join((s, c, RESET)) if s else c
        raise IndexError()

    def __add__(self, other):
        if not isinstance(other, (StyledText, StyledGroup)):
            other = StyledText(other)
        return StyledGroup(self, other)

    def __iadd__(self, other):
        if not isinstance(other, StyledText):
            other = StyledText(other)
        return StyledGroup(self, other)

    def __radd__(self, other):
        return StyledGroup(StyledText(text=other), self)


def _stylish_factory(ansi_sequence):
    def inner(text):
        return StyledText(text=text, style=ansi_sequence)

    return inner


# colors
blue = _stylish_factory('\x1b[94m')
green = _stylish_factory('\x1b[92m')
yellow = _stylish_factory('\x1b[93m')
red = _stylish_factory('\x1b[91m')
magenta = _stylish_factory('\x1b[95m')
cyan = _stylish_factory('\x1b[96m')
orange = _stylish_factory('\x1b[38;5;208m')

# styles
bold = _stylish_factory('\x1b[1m')
dim = _stylish_factory('\x1b[2m')
