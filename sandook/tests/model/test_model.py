__author__ = 'satmeet'
from sandook.model.model import ModelLocal as Model


def test_model_dict_not_None():
    m = Model()
    assert m._d is not None

def test_model_dict_default_one_tasklist():
    m = Model()
    print m.tasklists()
