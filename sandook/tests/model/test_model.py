__author__ = 'satmeet'
from sandook.model.model import ModelLocal as Model


class TestModel():

    def setUp(self):
        self.model = Model()

    def tearDown(self):
        pass

    def test_model_dict_not_None(self):
        assert self.model._d is not None

    def test_model_dict_default_one_tasklist(self):
        assert self.model.tasklists() == [("tasklist_1_id", "default")]

    def test_model_dict_default_one_tasklist_one_task(self):
        assert self.model.tasks("tasklist_1_id") == [("task_1_1_id",
                                                      "new task",
                                                      "z"*26,
                                                      "")]
    def test_model_add_tasklist(self):
        self.model.add_tasklist(title="tasklist2", tlist_id="tasklist_2_id")
        assert self.model.tasklists() == [("tasklist_1_id", "default"),
            ("tasklist_2_id", "tasklist2")]

    def test_model_add_task_to_tasklist1(self):
        self.model.add_task("tasklist_1_id", id="task_1_2_id",
                     title="new_task_list_1")
        assert self.model.tasks("tasklist_1_id") == [
            ("task_1_1_id", "new task", "z"*26, ""),
            ("task_1_2_id", "new_task_list_1", "z"*26, "")]

    def test_model_delete_only_tasklist(self):
        self.model.delete_tasklist("tasklist_1_id")
        #In this case we do not know the ID of the new tasklist but we can
        #check for title of the tasklist which will be auto generated
        assert self.model.tasklists()[0][1] == "default"

    def test_model_delete_tasklist2(self):
        self.model.add_tasklist(title="tasklist2", tlist_id="tasklist_2_id")
        self.model.delete_tasklist("tasklist_2_id")
        assert self.model.tasklists() == [("tasklist_1_id", "default")]

    def test_model_delete_task_from_tasklist1(self):
        self.model.delete_task("tasklist_1_id", "task_1_1_id")
        #In this case we do not know the ID of the new task but we can
        #check for title of the task which will be auto generated
        assert self.model.tasks("tasklist_1_id")[0][1] == "new task"

    def test_model_delete_second_task_from_tasklist1(self):
        self.model.add_task("tasklist_1_id", id="task_1_2_id",
                            title="new_task_list_1")
        self.model.delete_task("tasklist_1_id", "task_1_2_id")
        assert self.model.tasks("tasklist_1_id") == [("task_1_1_id",
                                                      "new task",
                                                      "z"*26,
                                                      "")]

    def test_model_update_tasklist1(self):
        self.model.update_tasklist("tasklist_1_id", title="testing list")
        assert self.model.tasklists() == [("tasklist_1_id", "testing list")]

    def test_model_update_task_in_tasklist1(self):
        self.model.update_task("tasklist_1_id", "task_1_1_id",
                               title="test task", position="a")
        assert self.model.tasks("tasklist_1_id") == [("task_1_1_id",
                                                      "test task",
                                                      "a",
                                                      "")]

