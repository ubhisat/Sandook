__author__ = 'satmeet'

import urwid


class HelpDialog(urwid.WidgetWrap):
    def __init__(self, callback, config=None):
        button = urwid.Padding(urwid.AttrMap(urwid.Button(u"Go back", on_press=callback), 'button'), align="center",
                               width=12)
        title = urwid.Padding(urwid.AttrMap(urwid.Text(u" Help Menu"), 'subheading'), align="center")
        h_text = urwid.Padding(urwid.Text(self.build_help_text(config), wrap="clip"), align="center", width=('relative',
                                                                                                             60))
        text = urwid.Padding(urwid.AttrMap(h_text, 'help'), align="center")
        holder = urwid.Pile([title, urwid.Divider(), text, urwid.Divider(), button])
        padding = urwid.Padding(holder, align="center", width=('relative', 50), min_width=100)
        filler = urwid.AttrMap(urwid.Filler(padding), 'help_border')
        self.__super.__init__(filler)

    def build_help_text(self, config):
        if config:
            import texttable as tt
            tab = tt.Texttable()
            header = ['Command', 'Key bindings']
            tab.header(header)

            d = config.get_key_bindings()
            for key in sorted(d.iterkeys()):
                tab.add_row([str(key),str(d[key])])

            tab.set_cols_width([30, 15])
            tab.set_cols_align(['c', 'r'])
            tab.set_cols_valign(['m', 'm'])
            tab.set_deco(tab.HEADER | tab.VLINES)
            tab.set_chars(['-','|','+','#'])
            return "\n\n" + tab.draw() + "\n\n"

        else:
            return "No help exists! Good Luck!"
