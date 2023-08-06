import re
from .datacleaner import *

# for the actual creating of CamelCase, which is easy
typicalbreaks = re.compile(r'[_\s]+(\w)')

# for tokenizing
humps = re.compile(r'([a-z])([A-Z0-9]+)')
numletter = re.compile(r'(\d)([a-zA-Z]+)')
letternum = re.compile(r'([a-zA-Z])(\d)')
acronym = re.compile(r'([A-Z]+)([A-Z]([a-r,t-z]|s(?:[a-zA-Z])))')

tokenre = re.compile(r'([A-Z]+s(?![a-r,t-z])|[A-Z]+(?![a-z])|[A-Z][a-z_]+|[a-z_]+|[^A-Za-z_]+)(.*)')

class CamelCase(DataCleaner):
    convert_numbers=False
    data_type=str

    def tokenize(self, val):
        val = val.strip()
        result = []
        while len(val):
            m = tokenre.match(val)
            if m:
                result.append(m.group(1))
                val = m.group(2)
            else:
                raise Exception("tokenre failed to match for " + val)
        return(result)

    def join(self, values):
        result = values[0]
        for val in values[1:]:
            result += val[0].upper() + val[1:]
        return(result)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.add_transliterations([
                (typicalbreaks, lambda m: m.group(1).upper()),
                # what about special characters?
        ])
