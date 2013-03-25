import os
# inspired from pyhn project at : https://github
# .com/socketubs/pyhn/blob/master/pyhn/config.py
try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser


class Config(object):
    def __init__(self, config_dir=None, config_file=None, db_file=None,
                 log_file=None):
        self.config_dir = config_dir
        self.config_file = config_file

        if config_dir is None:
            self.config_dir = os.path.join(
                os.environ.get('HOME', './'),
                '.sandook')
        if config_file is None:
            self.config_file = "config"

        if db_file is None:
            self.db_file = "pickledb"

        if log_file is None:
            self.log_file = "gtasks.log"

        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        self.config_path = os.path.join(self.config_dir, self.config_file)
        self.db_path = os.path.join(self.config_dir, self.db_file)
        self.log_path = os.path.join(self.config_dir, self.log_file)

        self.parser = SafeConfigParser()
        self.read()

    def read(self):
        self.parser.read(self.config_path)

        # Keybindings
        if not self.parser.has_section('keybindings'):
            self.parser.add_section('keybindings')

        if not self.parser.has_option('keybindings', 'list_operation'):
            self.parser.set('keybindings', 'list_operation', 'up,down')
        if not self.parser.has_option('keybindings', 'add_item'):
            self.parser.set('keybindings', 'add_item', 'ctrl n')
        if not self.parser.has_option('keybindings', 'move_up'):
            self.parser.set('keybindings', 'move_up', 'ctrl u')
        if not self.parser.has_option('keybindings', 'move_down'):
            self.parser.set('keybindings', 'move_down', 'ctrl d')
        if not self.parser.has_option('keybindings', 'finish_task'):
            self.parser.set('keybindings', 'finish_task', 'ctrl f')
        if not self.parser.has_option('keybindings', 'tasklist_edit'):
            self.parser.set('keybindings', 'tasklist_edit', 'e')
        if not self.parser.has_option('keybindings', 'tasklist_add'):
            self.parser.set('keybindings', 'tasklist_add', 'n')
        if not self.parser.has_option('keybindings', 'tasklist_delete'):
            self.parser.set('keybindings', 'tasklist_delete', 'd')
        if not self.parser.has_option('keybindings', 'show_help'):
            self.parser.set('keybindings', 'show_help', 'ctrl p')


        # Colors
        if not self.parser.has_section('colors'):
            self.parser.add_section('colors')

        if not self.parser.has_option('colors', 'body'):
            self.parser.set('colors', 'body', 'dark red|white|')
        if not self.parser.has_option('colors', 'focus'):
            self.parser.set('colors', 'focus', 'white|dark gray|standout')
        if not self.parser.has_option('colors', 'footer'):
            self.parser.set('colors', 'footer', 'black|dark gray')
        if not self.parser.has_option('colors', 'footer-error'):
            self.parser.set('colors', 'footer-error',
                            'dark red,bold|light gray')
        if not self.parser.has_option('colors', 'header'):
            self.parser.set('colors', 'header', 'dark gray,bold|white|')
        if not self.parser.has_option('colors', 'title'):
            self.parser.set('colors', 'title', 'dark red,bold|light gray')
        if not self.parser.has_option('colors', 'help'):
            self.parser.set('colors', 'help', 'black|dark magenta|standout')
        if not self.parser.has_option('colors', 'banner'):
            self.parser.set('colors', 'banner', 'black|light gray|standout')
        if not self.parser.has_option('colors', 'button'):
            self.parser.set('colors', 'button', 'black||standout|#f60|#f80')
        if not self.parser.has_option('colors', 'disabled'):
            self.parser.set('colors', 'disabled', 'dark gray|black|')
        if not self.parser.has_option('colors', 'task'):
            self.parser.set('colors', 'task', 'light gray|black|standout')
        if not self.parser.has_option('colors', 'subheading'):
            self.parser.set('colors', 'subheading',
                            'black,bold|yellow|standout')

        if not os.path.exists(self.config_path):
            self.parser.write(open(self.config_path, 'w'))

    def get_palette(self):
        palette = []
        for item in self.parser.items('colors'):
            name = item[0]
            settings = item[1]
            foreground = ""
            background = ""
            monochrome = ""
            high_f = ""
            high_b = ""
            if len(settings.split('|')) == 5:
                foreground = settings.split('|')[0]
                background = settings.split('|')[1]
                monochrome = settings.split('|')[2]
                high_f = settings.split('|')[3]
                high_b = settings.split('|')[4]
            if len(settings.split('|')) == 3:
                foreground = settings.split('|')[0]
                background = settings.split('|')[1]
                monochrome = settings.split('|')[2]
            elif len(settings.split('|')) == 2:
                foreground = settings.split('|')[0]
                background = settings.split('|')[1]
            elif len(settings.split('|')) == 1:
                foreground = settings.split('|')[0]

            palette.append((name, foreground, background, monochrome, high_f, high_b))
        return palette

    def get_key_bindings(self):
        bindings = {}
        for bind in self.parser.items('keybindings'):
            bindings[bind[0]] = bind[1]
        return bindings

