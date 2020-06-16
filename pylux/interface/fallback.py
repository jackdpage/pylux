class MessageBus:

    def __init__(self, config):
        self.config = config

    def post_feedback(self, line):
        print(self.get_pretty_line(line))

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


def main(interpreter):

    msg_bus = MessageBus(interpreter.config)
    interpreter.subscribe_client(msg_bus)

    while True:
        cmd = input('[pylux] ')
        interpreter.process_command(cmd)
