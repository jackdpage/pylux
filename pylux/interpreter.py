from pylux import document
from pylux.lib import printer


class Interpreter:
    def __init__(self, file, message_bus):
        self.file = file
        self.msg = message_bus

    def process_command(self, command):
        self.msg.post_feedback(command)
        keywords = command.split()
        obj = keywords[0]
        refs = keywords[1]
        action = keywords[2]
        if len(keywords) > 3:
            parameters = keywords[3:]
        else:
            parameters = []

        if action == 'Display' and refs == 'All':
            self.display_all(obj)

    def display_all(self, obj):
        lines = []
        if obj == 'All':
            objects = self.file
        else:
            objects = document.get_by_type(self.file, obj.lower())
        for i in objects:
            s = printer.get_generic_text_widget(i)
            lines.append(s)
        self.msg.post_output(lines)
