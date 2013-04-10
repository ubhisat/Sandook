__author__ = 'satmeet'

from sandook.model.tasklist import Tasklist
from sandook.model.task import Task
from os.path import basename
import utils
import datadb

def get_logger():
    from sandook.app.sulog import SULog
    return SULog().logw

class DropboxModel(object):
    def __init__(self, app_key, app_secret, access_key, access_secret, log=None):
        from dropbox import client, session
        ACCESS_TYPE = 'app_folder'
        self.sess = session.DropboxSession(app_key, app_secret, ACCESS_TYPE)
        self.sess.set_token(access_key, access_secret)
        self.cl = client.DropboxClient(self.sess)
        self.log = log

    def load(self, db_file, db_path):
        f, metadata = self.cl.get_file_and_metadata(db_file)
        self.log(metadata)
        out = open(db_path, 'w')
        out.write(f.read())
        out.close()
        f.close()

    def save(self, db_file, db_path):
        f = open(db_path)
        response = self.cl.put_file(db_file, f, overwrite=True)
        self.log(response)
        f.close()

class ModelLocal(object):
    def __init__(self, config=None, signal=None, log=None):
        self.dirty = False
        self.signal = signal
        self.config = config
        self.db_path = config.db_path if config \
            else '.sandookdb'
        self.log = lambda msg: log("%s : %s" % (basename(__file__), msg)) if log \
            else get_logger()
        try:
            if self.config.sync_enabled():
                access_key = self.config.parser.get('sync', 'key')
                access_secret = self.config.parser.get('sync', 'secret')
                app_key = self.config.parser.get('sync', 'app_key')
                app_secret = self.config.parser.get('sync', 'app_secret')
                self.log("%s %s %s %s" % (access_key, access_secret, app_key, app_secret))
                self.dropb = DropboxModel(app_key, app_secret, access_key, access_secret, log=self.log)
                self.dropb.load(self.config.db_file, self.db_path)

            with open(self.db_path, 'rb') as f:
                self._d = datadb.load(f)
        except IOError as ioe:
            self.log("Exception " + str(ioe))
            self.init_dict()
        except Exception as e:
            self.log("Runtime Exception " + str(e))
            self.init_dict()

    def init_dict(self):
        self.log("Initializing Dict with default values")
        self._d = dict()
        self._d['tasklists'] = dict()
        tlist = Tasklist(title="default")
        self._d['tasklists'][tlist.id] = tlist
        task = Task(title="new task")
        self._d['tasklists'][tlist.id].tasks[task.id] = task
        self.dirty = True
        self.save()

    def tasklists(self):
        retd = []
        for tlid in self._d['tasklists'].keys():
            retd.append((self._d['tasklists'][tlid].id,
                         self._d['tasklists'][tlid].title))
        if len(retd) == 0:
            self.log("Did not find any tasklists, creating new")
            new_tasklist = self.add_tasklist(title="default")
            retd = [(new_tasklist.id, new_tasklist.title)]

        return retd

    def tasks(self, tasklist):
        self.log(self._d['tasklists'][tasklist].tasks)
        retd = []
        d = self._d['tasklists'][tasklist].tasks
        for tid in sorted(d, key=lambda x: d[x].completed):
            retd.append((self._d['tasklists'][tasklist].tasks[tid].id,
                         self._d['tasklists'][tasklist].tasks[tid].title,
                         self._d['tasklists'][tasklist].tasks[tid].position,
                         self._d['tasklists'][tasklist].tasks[tid].completed)
                        )
        if len(retd) == 0:
            self.log("Did not find any tasks, creating new")
            new_task = self.add_task(tasklist, title="new task")
            retd = [(new_task.id, new_task.title, new_task.position, new_task.completed)]
        return retd

    def add_tasklist(self, title, tlist_id=None):
        tlist = Tasklist(title=title, id=tlist_id) if tlist_id else \
                Tasklist(title=title)
        self._d['tasklists'][tlist.id] = tlist
        self.add_task(tlist.id, title="")
        return tlist

    def add_task(self, tasklist, **kwargs):
        task = Task(**kwargs)
        self._d['tasklists'][tasklist].tasks[task.id] = task
        self.dirty = True
        return task

    def update_tasklist(self, tasklist, **kwargs):
        if kwargs.get('title', None):
            self._d['tasklists'][tasklist].title = kwargs['title']
        if kwargs.get('updated', None):
            self._d['tasklists'][tasklist].updated = kwargs['updated']
        self.dirty = True

    def update_task(self, tasklist, task, **kwargs):
        self.log("update task %s" % task)
        if kwargs.get('title', None):
            self._d['tasklists'][tasklist].tasks[task].title = kwargs['title']
        if kwargs.get('position', None):
            self._d['tasklists'][tasklist].tasks[task].position = kwargs[
                'position']
        if kwargs.get('updated', None):
            self._d['tasklists'][tasklist].tasks[task].updated = kwargs[
                'updated']
        if kwargs.get('completed', None):
            comp = kwargs['completed'] if kwargs['completed'] != 'x' else ''
            self._d['tasklists'][tasklist].tasks[task].completed = comp
        if kwargs.get('hidden', None):
            self._d['tasklists'][tasklist].tasks[task].hidden = kwargs[
                'hidden']
        if kwargs.get('deleted', None):
            self._d['tasklists'][tasklist].tasks[task].deleted = kwargs[
                'deleted']
        self.dirty = True

    def save(self):
        self.dirty = True
        if self.dirty:
            self.log("Saving...")
            with open(self.db_path, 'wb') as f:
                #pickle.dump(self._d, f)
                datadb.dump(self.to_json(), f)
            # Remote sync
            if self.config.sync_enabled() and self.dropb:
                self.dropb.save(self.config.db_file, self.db_path)
            self.log("Saved...")
            self.dirty = False
        else:
            print "not saving"
            self.log("Dirty bit not set, not saving...")

    def delete_tasklist(self, tasklist):
        del(self._d['tasklists'][tasklist])
        self.dirty = True

    def delete_task(self, tasklist, task):
        del(self._d['tasklists'][tasklist].tasks[task])
        self.dirty = True

    def to_json(self):
        return utils.get_json_repr(self._d)

