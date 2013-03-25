__author__ = 'satmeet'

import utils

class Task(object):
    """
    Tasks
    {
      "kind": "tasks#task",
      "id": string,
      "etag": etag,
      "title": string,
      "updated": datetime,
      "selfLink": string,
      "parent": string,
      "position": string,
      "notes": string,
      "status": string,
      "due": datetime,
      "completed": datetime,
      "deleted": boolean,
      "hidden": boolean,
      "links": [
        {
          "type": string,
          "description": string,
          "link": string
        }
      ]
    }
    """
    def __init__(self, **kw):
        self.kind = "tasks#task"
        self.id = kw.get('id', utils.get_id())
        self.etag = kw.get('etag', "ETAG-%s" % self.id)
        self.title = kw.get('title', '')
        self.updated = kw.get('updated', utils.now())
        self.selfLink = kw.get('selfLink', "self_link_not_implemented")
        self.parent = kw.get('parent', '')
        self.position = kw.get('position', 'z' * 26)
        self.notes = kw.get('notes', '')
        self.status = kw.get('status', '')
        self.due = kw.get('due', '')
        self.completed = kw.get('completed', '')
        self.deleted = kw.get('deleted', '')
        self.hidden = kw.get('hidden', '')
        self.links = [] # Not Impl.

    def __repr__(self):
        return utils.get_json_repr(self.__dict__)
