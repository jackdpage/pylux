import wx
from pylux.lib import autocomplete


class MessageBus:

    def __init__(self, window, config):
        self.app = window
        self.config = config

    def post_feedback(self, line):
        self.app.SetStatusText(self.get_pretty_line(line))

    def post_output(self, lines, **kwargs):
        for l in lines:
            print(self.get_pretty_line(l))

    def get_pretty_line(self, l):
        if type(l) == str:
            return l
        s = ''
        for i in l:
            if type(i) == str:
                s += i
            elif type(i) == tuple:
                colour = self.config['fallback-colours'].get(i[0], '0')
                s = s + '\033[' + colour + 'm' + i[1] + '\033[m'
        return s


class Autocompleter(wx.TextCompleter):

    def __init__(self, interpreter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interpreter = interpreter
        # Setting this instance variable of _i is a super hacky way of
        # doing this, but due to the requirements of the pure functions,
        # there doesn't seem to be much other way of doing it
        self._i = None
        self._pre = None

    def Start(self, prefix):
        self._pre = prefix
        self._i = -1
        return bool(self.interpreter.get_expected_input(self._pre, check_partial=True))

    def GetNext(self):
        try:
            self._i += 1
            return self._pre + self.interpreter.get_expected_input(self._pre, check_partial=True)[self._i]
        except IndexError:
            return ''


class CommandLine(wx.TextCtrl):

    def __init__(self, interpreter, *args, **kwargs):
        super().__init__(*args, style=wx.TE_PROCESS_ENTER, **kwargs)
        self.AutoComplete(Autocompleter(interpreter))

    def clear(self):
        self.SetValue('')


class Application(wx.App):

    def __init__(self, interpreter, *args, **kwargs):
        self.interpreter = interpreter
        self.file = interpreter.file
        self.config = interpreter.config
        self.message_bus = None
        self._window = None
        self._cmd = None
        self.post = interpreter.process_command
        super().__init__(*args, **kwargs)

    def OnInit(self):
        self._window = wx.Frame(None, title='Pylux')
        self._window.Show()
        self._window.CreateStatusBar()
        panel = wx.Panel(self._window)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._cmd = CommandLine(self.interpreter, panel)
        self._cmd.Bind(wx.EVT_TEXT_ENTER, self.process_command)
        sizer.Add(self._cmd)
        panel.SetSizer(sizer)
        self.SetTopWindow(self._window)
        self.subscribe()
        return True

    def subscribe(self):
        self.message_bus = MessageBus(self._window, self.config)
        self.interpreter.subscribe_client(self.message_bus)

    def process_command(self, evt):
        self.post(evt.GetString())
        self._cmd.clear()


def main(interpreter):

    app = Application(interpreter)
    app.MainLoop()
