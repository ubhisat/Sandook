__author__ = 'satmeet'

import urwid


class ListWidget(urwid.WidgetWrap):
    def __init__(self, title, elements=None, callback=None):
        self.elements = elements
        self.title = title
        self._render(callback)

    def _render(self, callback):
        holder = [
                urwid.Padding(
                    urwid.AttrMap(urwid.Padding(urwid.Text(self.title),
                                                width=('relative', 100),
                                                align='center'),
                                  'subheading', focus_map='subheading'),
                width=('relative', 50),
                align='center'
            ),
            urwid.Divider(),
            urwid.Divider()
        ]

        #Get the size of the widest text and space the list buttons accordingly
        wid = max([len(x[1]) for x in self.elements]) + 8
        for item in self.elements:
            button = urwid.Button(item[1])
            urwid.connect_signal(button, "click", callback, [str(item[0]), str(item[1])])
            holder.append(
                urwid.Padding(
                    urwid.AttrMap(urwid.Padding(button, width=wid,align='center'
                    ), None, focus_map='focus'), width=wid,
                    align='center'
                )
            )
        self.widget = urwid.ListBox(urwid.SimpleFocusListWalker(holder))
        urwid.WidgetWrap.__init__(self, self.widget)

    def focus_tasklist_id(self):
        return self.elements[self.widget.focus_position - 3]
