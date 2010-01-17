import re

class RegexPattern(object):
    def __init__(self, regex, name=''):
        self.regex = re.compile(regex, re.UNICODE)
        self.name = name
    
    def resolve(self, string):
        match = self.regex.search(string)
        if match:
            return self.name, match.groupdict()

class patterns(object):
    def __init__(self, unknown, *args):
        self.patterns = []
        self.unknown = unknown
        
        for pattern in args:
            if pattern.__class__ == str:
                self.patterns.append(RegexPattern(pattern))
            else:
                self.patterns.append(RegexPattern(*pattern))
    
    def resolve(self, name):
        for pattern in self.patterns:
            match = pattern.resolve(name)
            if match:
                return match
        return self.unknown