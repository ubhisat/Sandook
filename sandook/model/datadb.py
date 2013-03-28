__author__ = 'satmeet'

import json
from tasklist import Tasklist
from task import Task

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
