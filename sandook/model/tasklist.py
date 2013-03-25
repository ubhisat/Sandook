__author__ = 'satmeet'
__version__ = "0.1"

import utils

"""
Model class for tasklist.
Will create json from it.
"""

class Tasklist(object):
    """
    Model for class, tasklist resource representation
    {
      "kind": "tasks#taskList",
      "id": string,
      "etag": string,
      "title": string,
      "updated": datetime,
      "selfLink": string
    }

    """
    def __init__(self, **kw):
        self.id = kw.get('id', utils.get_id())
        self.etag = kw.get('etag', "ETAG-%s" % self.id)
        self.title = kw.get('title', '')
        self.updated = kw.get('updated', utils.now())
        self.selfLink = kw.get('selfLink', "self_link_url_not_implemented")
        self.tasks = {}
        self.kind = "tasks#taskList"

    def __repr__(self):
        return utils.get_json_repr(self.__dict__)
