__author__ = 'satmeet'

import urwid
from os.path import basename

class TaskWidget(urwid.WidgetWrap):
    """
    class to represent individual task
    """
    class CEdit(urwid.Edit):
        def keypress(self, size, key):
            if key == 'backspace'and \
                    self.get_cursor_coords((10,))[0] < 0:
                pass
            elif key != 'enter':
                super(TaskWidget.CEdit, self).keypress(size, key)

    '''
    Auto update the text colors. using palette from config.
    '''

    def __init__(self, task, callback, change_callback, signal, bindings, logw):
        self.logw = lambda msg: logw("%s : %s" % (basename(__file__), msg))
        self.task = task
        self.taskid = task[0]
        self.title = task[1]
        self.pos = task[2]
        self._callback = callback
        self.edit = TaskWidget.CEdit(edit_text=self.title)
        urwid.connect_signal(self.edit, "change", change_callback, None)
        self.disabled = task[3]
        self.chkbox = urwid.CheckBox("", state=self.disabled)
        self.signal = signal
        self.bindings = bindings
        self.refresh()

    def keypress(self, size, key):
        if key in self.bindings['finish_task'].split(','):
            self.chkbox.set_state(not(self.chkbox.get_state()),
                                  do_callback=False)
            self.disabled = not self.disabled
            self.refresh()
            self.logw(" UI widget - " + key)
            self.signal.send_signal('task_complete')
        elif key in self.bindings['add_item'].split(','):
            self.logw(" UI : key detected")
            self.signal.send_signal('add_item')
        elif key in self.bindings['move_up'].split(','):
            self.logw(" UI : move up key detected")
            self.signal.send_signal('move_up')
        elif key in self.bindings['move_down'].split(','):
            self.logw(" UI : move down key detected")
            self.signal.send_signal('move_down')
        elif key in self.bindings['toggle_complete'].split(','):
            self.logw(" UI : toggle_complete tasks")
            self.signal.send_signal('toggle_complete')
        elif key in self.bindings['delete_task'].split(','):
            self.logw(" UI : delete task")
            self.signal.send_signal('delete_task')
        elif key in self.bindings['show_tasklists'].split(','):
            self.logw(" UI : show tasklists")
            self.signal.send_signal('show_tasklists')
        elif key == 'enter':
            self._callback(None, [self.task, self.edit.get_edit_text()])
        elif not ((key in self.bindings['list_operation'].split(',')) or
             (key in self.bindings['show_help'].split(','))):
            if not self.disabled:
                self.edit.keypress(size, key)
        else:
            return key

    def __len__(self):
        return len(self.edit.get_edit_text())

    def refresh(self):
        state = 'disabled' if self.disabled else 'task'
        self.widget = urwid.Columns([
            (5, urwid.AttrMap(self.chkbox, state, focus_map='focus')),
            ('weight', 1, urwid.AttrMap(self.edit, state, focus_map='focus')),
        ], min_width=5)
        self.widget.focus_position = 1
        urwid.WidgetWrap.__init__(self, self.widget)

    def values(self):
        return self.taskid, self.edit.get_edit_text(), self.pos, self.disabled

