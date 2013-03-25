__author__ = 'satmeet'

import urwid


class QuestionBoxW(urwid.WidgetWrap):
    class CEdit(urwid.Edit):
        def keypress(self, size, key):
            if key != 'enter':
                return super(QuestionBoxW.CEdit, self).keypress(size, key)

    def __init__(self, question, edit_text, button_text=u"Search",
                 callback=None, cancel_button_text=None, cancel_callback=None):
        if len(edit_text) > 0:
            self.question = QuestionBoxW.CEdit(question + " =>        ")
            self.question.edit_text = edit_text
        else:
            self.question = urwid.Text(question)
        #Add event handler. (Submit in this case)
        self.question._on_button = self._on_button
        self.button = urwid.Button(button_text)
        if cancel_button_text:
            self.cancel_button = urwid.Button(cancel_button_text)
        else:
            self.cancel_button = None
        self.widget = self._render(callback, cancel_callback)
        self._callback = callback
        self._cancel_callback = cancel_callback
        self.__super.__init__(self.widget)

    def _render(self, callback, cancel_callback):
        urwid.connect_signal(self.button, "click", self._on_button)
        if cancel_callback:
            urwid.connect_signal(self.cancel_button, "click", self._on_cancel_button)

        #Add display properties to elements
        b_width = len(self.button.get_label()) + 7
        if self.cancel_button:
            holder = urwid.Pile([
                urwid.AttrMap(self.question, 'edit'),
                urwid.Divider(),
                urwid.Divider(),
                urwid.Columns([
                    urwid.Padding(urwid.AttrMap(self.button, 'button'), width=b_width, align="right"),
                    urwid.Padding(urwid.AttrMap(self.cancel_button, 'button'), width=b_width, align="left")],
                    dividechars=2, focus_column=0
                )
            ])
        else:
            holder = urwid.Pile([
                urwid.AttrMap(self.question, 'edit'),
                urwid.Divider(),
                urwid.Divider(),
                urwid.Columns([
                    urwid.Padding(urwid.AttrMap(self.button, 'button'), width=b_width, align="center")],
                    dividechars=2, focus_column=0
                )
            ])
        padding = urwid.Padding(holder, align="center", width=('relative', 50))
        return urwid.Filler(padding)

    def _on_button(self, button):
        response = self.question.get_edit_text() if isinstance(self.question, QuestionBoxW.CEdit) else None
        self._callback(button, response)

    def _on_cancel_button(self, button):
        self._cancel_callback(button, None)
