__author__ = 'satmeet'

"""
Utility funcitons
"""
import json
from sandook.model.tasklist import Tasklist
from sandook.model.task import Task

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

def load(fd):
    try:
        t = fd.readlines()[0] # It should be only one line data
        dd = json.loads(t)
        _d = dict()
        _d['tasklists'] = dict()
        for tasklist in dd['tasklists']:
            td = dd['tasklists'][tasklist]
            t = Tasklist(**td)
            for task in td['tasks']:
                taskitem = Task(**td['tasks'][task])
                t.tasks[taskitem.id] = taskitem
            _d['tasklists'][t.id] = t
        return _d
    except:
        raise Exception("loading from db failed")

def dump(model_dict, fd):
    fd.write(model_dict)
    pass