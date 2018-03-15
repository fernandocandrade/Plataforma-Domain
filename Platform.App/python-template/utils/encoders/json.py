from flask.json import JSONEncoder
import calendar
import datetime


class Encoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime.date) or isinstance(obj, datetime.datetime) or isinstance(obj, datetime.time):
                return obj.isoformat()
        except TypeError:
            pass
        return JSONEncoder.default(self, obj)