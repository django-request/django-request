# -*- coding: utf-8 -*-
import re

from six import string_types


class RegexPattern(object):
    def __init__(self, regex, name=''):
        self.regex = re.compile(regex, re.UNICODE)
        self.name = name

    def resolve(self, string):
        match = self.regex.search(string)
        if match:
            return self.name, match.groupdict()


class Patterns(object):
    def __init__(self, unknown, *args):
        self.patterns = ()
        self.unknown = unknown

        for pattern in args:
            if isinstance(pattern, string_types):
                self.patterns += (RegexPattern(pattern),)
            else:
                self.patterns += (RegexPattern(*pattern),)

    def resolve(self, name):
        for pattern in self.patterns:
            match = pattern.resolve(name)
            if match:
                return match
        return self.unknown
