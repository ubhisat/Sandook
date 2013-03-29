__author__ = 'satmeet'
from sandook.model.model import ModelLocal as Model
from nose.tools import with_setup

class TestModel():

    def setUp(self):
        self.m = Model()

    def tearDown(self):
        pass

    def test_model_dict_not_None(self):
        assert self.m._d is not None

    def test_model_dict_default_one_tasklist(self):
        assert self.m.tasklists() == [("tasklist_1_id", "default")]

    def test_model_dict_default_one_tasklist_one_task(self):
        assert self.m.tasks("tasklist_1_id") == [("task_1_1_id", "new task",
                                              "z"*26,
                                             "")]
    def test_model_add_tasklist(self):
        self.m.add_tasklist(title="tasklist2", tlist_id="tasklist_2_id")
        assert self.m.tasklists() == [("tasklist_1_id", "default"),
            ("tasklist_2_id", "tasklist2")]

    def test_model_add_task_to_tasklist1(self):
        self.m.add_task("tasklist_1_id", id="task_1_2_id",
                     title="new_task_list_1")
        assert self.m.tasks("tasklist_1_id") == [
            ("task_1_1_id", "new task", "z"*26, ""),
            ("task_1_2_id", "new_task_list_1", "z"*26, "")]
