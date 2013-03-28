__author__ = 'satmeet'

"""
Utility funcitons
"""

def get_id(size=6):
    import random
    import string

    return ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in
        range(size))

def now():
    import datetime
    #Date should be in the RFC3339 format
    #'2008-04-02T20:00:00Z' Z means local offset is zero hence UTC timezone
    return datetime.datetime.utcnow().isoformat(sep="T") + "Z"

def get_json_repr(d):
    for key, value in d.iteritems():
        if value is None:
            value = ""
        elif isinstance(value, bool):
            value = str(value)
        d[key] = value
    return str(d).replace("'", "\"").replace('u"', '"')

