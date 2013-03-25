__author__ = 'satmeet'

from threading import Timer

import urwid
from sandook.view.taskwidget import TaskWidget
from sandook.view.listwidget import ListWidget
from sandook.view.questionbox_w import QuestionBoxW
from signals import CSignal
from sandook.model import utils
from sandook.view.helpdialog import HelpDialog
from os.path import basename


class App(object):

    def __init__(self, config, model, logw):
        self.logw = lambda msg: logw(basename(__file__) + ": " + str(msg))
        self.model = model
        self.csignal = CSignal()
        self.config = config
        self.bindings = self.config.get_key_bindings()
        self.tasklists = []
        self.current_tasklist = None
        self.tasks = []
        self.mbody = None
        self.help_visible = False
        self.tasks_visible = False
        self.build(init=True)
        self.setup_signals()
        self.dirty = False
        self.timer = Timer(2, self.on_timer)
        self.idle_time = 0
        self.show_completed = False

    def build_body(self):
        self.filler = urwid.Filler(self.listbox, valign="middle",
                                   height=('relative', 100),
                                   top=2, min_height=10)
        if self.mbody is not None:
            self.mbody.original_widget = self.filler
        else:
            #TODO: check logic
            self.mbody = urwid.AttrMap(urwid.Filler(self.listbox, valign="middle",
                                       height=('relative', 100),
                                       top=2, min_height=10), 'body')

    def build_tasks(self):
        self.walker = urwid.SimpleListWalker(self.tasks)
        self.listbox = urwid.ListBox(self.walker)
        self.update_header("Tasklist: " + self.current_tasklist_title)
        self.build_body()
        self.tasks_visible = True

    def build(self, init=False):
        self.tasklists = self.model.tasklists()
        self.listbox = ListWidget(u"  Please select a list",
                                  self.tasklists, self.on_list_select)
        self.build_body()
        if init:
            self.set_top(self.mbody)
            self.build_header("Sandook(ToDo)")
            self.build_footer(self.config.get_help_text())
            self.frame = urwid.Frame(self.top, header=self.header,
                                     footer=self.footer)
        else:
            self.update_footer('Status:')
            self.update_header('Sandook(ToDo)')
        self.tasks_visible = False

    def build_edit_tasklist(self, sel_tasklist):
        qbox = QuestionBoxW(question=u"Rename TaskList",
                            edit_text=sel_tasklist[1], button_text="Edit",
                            callback=self.on_sel_tasklist_edit,
                            cancel_button_text="Cancel",
                            cancel_callback=self.on_tasklist_edit_cancel)
        self.mbody.original_widget = qbox

    def build_add_tasklist(self):
        qbox = QuestionBoxW(question=u"New TaskList name",
                            edit_text=" ", button_text="Add",
                            callback=self.on_tasklist_add,
                            cancel_button_text="Cancel",
                            cancel_callback=self.on_tasklist_add_cancel)
        self.mbody.original_widget = qbox

    def build_delete_tasklist(self, sel_tasklist):
        qbox = QuestionBoxW(question=u"Are you sure, you want to delete the tasklist '%s'? This will also delete"
                                     u"all the tasks." % sel_tasklist[1],
                            edit_text="", button_text="Yes",
                            callback=self.on_tasklist_delete,
                            cancel_button_text="No",
                            cancel_callback=self.on_tasklist_delete_cancel)
        self.mbody.original_widget = qbox

    def build_delete_task(self):
        sel_task = self.listbox.focus
        self._original_w = self.mbody.original_widget
        qbox = QuestionBoxW(question=u"Are you sure, you want to delete the task: '%s'?"
                                     u" You can also mark it as complete" % sel_task.title,
                            edit_text="", button_text="Yes",
                            callback=self.on_task_delete,
                            cancel_button_text="No",
                            cancel_callback=self.on_task_delete_cancel)
        self.mbody.original_widget = qbox

    def build_help_dialog(self):
        self._original_w = self.mbody.original_widget
        helpd = HelpDialog(config=self.config, callback=self.on_help_exit)
        self.mbody.original_widget = helpd
        self.help_visible = True

    def build_header(self, header):
        self.header = urwid.AttrMap(
            urwid.Pile([urwid.Text(('header', header),
                                   align='center', wrap='any'),
                        urwid.Divider(div_char='.')]),
            'header'
        )

    def build_footer(self, help_text):
        self.footer = urwid.AttrMap(urwid.Columns([
                             urwid.Padding(urwid.Text(u"Status"), width=('relative', 70), align="left"),
                             urwid.Padding(urwid.Text(u"For Commands, press : %s  " % help_text), width='pack',
                                           min_width=len(help_text) + 24, align="right")],
            dividechars=2, focus_column=0), 'footer')

    def update_header(self, text):
        #This needs to be modified if footer structure is changed.
        self.header.original_widget.contents[0][0].set_text(text)

    def update_footer(self, text):
        #This needs to be modified if footer structure is changed.
        self.footer.original_widget.contents[0][0].original_widget.set_text(text)

    def set_top(self, widget):
        self.top = urwid.Overlay(widget, urwid.SolidFill(' '),
                                 align='center',
                                 width=('relative', 95),
                                 valign='middle',
                                 height=('relative', 95),
                                 min_width=20, min_height=10)

    def setup_signals(self):
        urwid.connect_signal(self.csignal, 'task_complete',
                             self.on_task_completed)
        urwid.connect_signal(self.csignal, 'add_item',
                             self.on_add_item)
        urwid.connect_signal(self.csignal, 'move_up',
                             self.on_move_up)
        urwid.connect_signal(self.csignal, 'move_down',
                             self.on_move_down)
        urwid.connect_signal(self.csignal, 'input_recv',
                             self.on_input_recv)
        urwid.connect_signal(self.csignal, 'show_tasklists',
                             self.on_show_tasklists)
        urwid.connect_signal(self.csignal, 'toggle_complete',
                             self.on_toggle_complete)
        urwid.connect_signal(self.csignal, 'delete_task',
                             self.build_delete_task)

    def exit_program(self, button):
        self.cancel_timer_thread()
        self.save()
        urwid.ExitMainLoop()

    def on_show_tasklists(self):
        self.save()
        self.build()

    def on_toggle_complete(self):
        self.show_completed = not self.show_completed
        self.tasks = []
        self.build_taskwidgets()

    def on_help_exit(self, button):
        self.help_visible = False
        self.mbody.original_widget = self._original_w

    def on_tasklist_add(self, button, arg):
        self.logw("Add tasklist "+ arg)
        self.model.add_tasklist(title=arg)
        self.build()

    def on_tasklist_add_cancel(self, button, arg):
        self.logw("Cancel tasklist add")
        self.build()

    def on_tasklist_edit_cancel(self, button, arg):
        self.logw("Cancel tasklist edit")
        self.build()

    def on_tasklist_delete(self, button, arg):
        self.logw("Delete tasklist "+ str(self.sel_tasklist_edit[1]))
        self.model.delete_tasklist(self.sel_tasklist_edit[0])
        self.build()

    def on_task_delete(self, button, arg):
        self.logw("Delete task*  "+ str(self.listbox.focus.title))
        self.logw("Delete task* :  "+ str(self.listbox.focus.taskid)+ " " + self.current_tasklist)
        self.model.delete_task(self.current_tasklist, self.listbox.focus.taskid)
        self.tasks = []
        self.build_taskwidgets()

    def on_tasklist_delete_cancel(self, button, arg):
        self.logw("Cancel tasklist delete")
        self.build()

    def on_task_delete_cancel(self, button, arg):
        self.logw("Cancel task delete")
        self.mbody.original_widget = self._original_w

    def on_task_enter(self, button, arg):
        curr_task = self.listbox.focus
        self.model.update_task(self.current_tasklist, curr_task.taskid, title=curr_task.title)
        self.update_footer('Saved: %s' % arg[1])

    def keystroke(self, key):
        self.logw("Pres: keypress %s " % key)
        if key in self.bindings['show_help'] and not self.help_visible:
            self.build_help_dialog()
        elif self.tasks_visible:
            self.listbox.focus.keypress(None, key)
        else:
            if key in self.bindings['tasklist_edit'] and not self.help_visible:
                self.sel_tasklist_edit = self.listbox.focus_tasklist_id()
                self.logw(key + str(self.sel_tasklist_edit[0:2]))
                self.build_edit_tasklist(self.sel_tasklist_edit)
            elif key in self.bindings['tasklist_add'] and not self.help_visible:
                self.build_add_tasklist()
            elif key in self.bindings['tasklist_delete'] and not self.help_visible:
                self.sel_tasklist_edit = self.listbox.focus_tasklist_id()
                self.logw(key + str(self.sel_tasklist_edit[0:2]))
                self.build_delete_tasklist(self.sel_tasklist_edit)

    def on_sel_tasklist_edit(self, button, arg):
        self.logw("On_Sel_tasklist_edit  " + arg)
        self.model.update_tasklist(self.sel_tasklist_edit[0], title=arg)
        self.save()
        self.build()

    def on_list_select(self, button, arg):
        self.current_tasklist = arg[0]
        self.current_tasklist_title = arg[1]
        self.logw("Select tasklist %s :" % arg)
        self.tasks = []
        self.build_taskwidgets()

    def build_taskwidgets(self):
        ret_tasks = self.model.tasks(self.current_tasklist)
        for item in ret_tasks:
            self.logw(item)
            comp = False if item[3] == '' else True
            item_list = list(item)
            item_list[3] = comp
            self.logw(" show_completed %s, comp %s::  " % (str(self.show_completed), str(comp)))
            if not (self.show_completed and comp):
                self.logw(" adding Task::  " + str(item_list))
                self.tasks.append(TaskWidget(task=item_list,
                                             callback=self.on_task_enter,
                                             change_callback=self.on_input_recv,
                                             signal=self.csignal,
                                             bindings=self.bindings,
                                             logw=self.logw))

        #Check is self.tasks is empty. If yes, create one
        if len(self.tasks) == 0:
            self.on_add_item()
        self.build_tasks()

    def on_timer(self):
        self.idle_time += 1
        if self.idle_time > 4:
            self.idle_time = 0
            self.logw("save() called")
            self.save()
        else:
            self.timer = Timer(2, self.on_timer)
            self.timer.start()

    def on_input_recv(self, button, arg):
        self.logw("Pres : input received, clearing dirty data\n")
        self.dirty = False
        self.idle_time = 0
        if hasattr(self, 'timer'):
            self.logw("thread exists")
            if self.timer.isAlive():
                self.logw("Thread is active, cancel thread")
                self.timer.cancel()
        self.timer = Timer(2, self.on_timer)
        self.timer.start()
        self.logw("thread started:")

    def save(self):
        if not self.dirty:
            self.logw('save this shit!!')
            if self.tasks_visible:
                for twidget in self.tasks:
                    self.logw("Test save count (tasks) " + str(twidget.values()))
                    tt = twidget.values()
                    task_title = tt[1]
                    comp = 'x' if not tt[3] else utils.now()
                    # Only save tasks which are not empty
                    if len(task_title) > 0:
                        self.model.update_task(self.current_tasklist, tt[0],
                                               title=task_title,
                                               position=tt[2],
                                               completed=comp)
            self.model.save()
            self.dirty = False
        else:
            self.logw('Dirty data exists: CANNOT *save* this shit!!')

    def on_move_up(self):
        pos = self.listbox.focus_position
        if (pos - 1) < 0:
            return
        self.logw('Pres:  Move up item')
        tw = self.walker.pop(pos)
        pos -= 1
        self.walker.insert(pos, tw)
        self.listbox.focus_position = pos

    def on_move_down(self):
        pos = self.listbox.focus_position
        if (pos + 1) > len(self.walker.positions()) - 1:
            return
        self.logw('Pres:  Move down item')
        tw = self.walker.pop(pos)
        pos += 1
        self.walker.insert(pos, tw)
        self.listbox.focus_position = pos

    def on_add_item(self):
        if not self.dirty:
            self.logw('Add new item')
            nt = self.model.add_task(self.current_tasklist, title='')
            comp = False if nt.completed == '' else True
            tw = TaskWidget([nt.id, nt.title, nt.position, comp],
                            callback=self.on_task_enter,
                            change_callback=self.on_input_recv,
                            signal=self.csignal,
                            bindings=self.bindings, logw=self.logw)
            self.tasks.append(tw)
            pos = self.listbox.focus_position + 1
            self.walker.insert(pos, tw)
            self.listbox.focus_position = pos
            self.dirty = True
        else:
            self.logw('Dirty data exists: Cannot add new item')

    def on_task_completed(self):
        taskid = self.listbox.focus.taskid
        completed = self.listbox.focus.values()[3]
        self.logw(' Received Signal,  Will mark the task %s as complete: %s' % (self.listbox.focus.taskid, str(completed)))
        comp_val = 'x' if not completed else utils.now()
        self.model.update_task(self.current_tasklist, taskid, completed=comp_val)
        update_text = 'complete' if completed else 'uncomplete'
        self.update_footer('Task "%s" marked as %s' %
                           (self.listbox.focus.title, update_text))

    def cancel_timer_thread(self):
        if self.timer and self.timer.isAlive():
            self.timer.cancel()

    def main(self):
        try:
            self.loop = urwid.MainLoop(self.frame,
                                       palette=self.config.get_palette(),
                                       unhandled_input=self.keystroke,
                                       handle_mouse=False)
            self.loop.screen.set_terminal_properties(256)
            self.loop.run()
        except(KeyboardInterrupt, SystemExit):
            self.exit_program(None)
