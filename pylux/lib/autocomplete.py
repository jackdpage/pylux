from pylux.document import COMMAND_STR_MAP
import pylux.lib.keyword as kw


class Keymapper:

    def __init__(self, interpreter, config):
        self.interpreter = interpreter
        self.keys = {}
        for k, v in config['autocomplete'].items():
            if k in kw.__dict__:
                self.keys[kw.__dict__[k]] = v

        self.enabled = True

    def _generate_keymap(self, tuple_list, pre='', post=' '):
        keymap = {}
        for i in tuple_list:
            keymap[i[1]] = pre + i[0] + post
        return keymap

    def get_keymap(self, fragment):
        relevant_keys = []
        n = len(fragment.split())
        expected_input = self.interpreter.get_expected_input(fragment)
        if expected_input:
            for exp in expected_input:
                if exp in self.keys:
                    relevant_keys.append((exp, self.keys[exp]))

        # Add on extra commands which are not covered by the interpreter
        # Double-type an object type to switch context to that
        if n == 1:
            k1 = fragment.split()[0]
            if k1 in COMMAND_STR_MAP:
                relevant_keys.append((k1, self.keys[k1]))

        # We need to add on a pre-space to the keyword if it is appearing after the
        # refs field (i.e. if the current command length is 2). Also just return None
        # if there are no relevant keys.
        if not relevant_keys:
            return None
        if n == 0 or n == 1:
            return self._generate_keymap(relevant_keys)
        elif n == 2:
            return self._generate_keymap(relevant_keys, pre=' ')

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def toggle(self):
        self.enabled = not self.enabled
