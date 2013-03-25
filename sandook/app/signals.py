import urwid.signals


class CSignal (object):
    __metaclass__ = urwid.signals.MetaSignals
    signals = ['task_complete', 'input_recv', 'add_item', 'move_up',
               'move_down', 'show_tasklists', 'toggle_complete',
               'delete_task',]

    def send_signal(self, update):
        urwid.emit_signal(self, update)
