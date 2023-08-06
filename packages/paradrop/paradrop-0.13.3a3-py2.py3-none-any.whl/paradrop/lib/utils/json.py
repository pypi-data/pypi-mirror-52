from __future__ import absolute_import
from .json import JSONEncoder


class ParadropJSONEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'asdict'):
            return o.asdict()

        try:
            return JSONEncoder.default(self, o)
        except TypeError:
            return o.__dict__
