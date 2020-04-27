class Keymapper:

    def __init__(self, interpreter, config):
        self.interpreter = interpreter
        self.keys = config['autocomplete']
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
        if not expected_input:
            return None
        for exp in expected_input:
            if exp in self.keys:
                relevant_keys.append((exp, self.keys[exp]))
        # We need to add on a pre-space to the keyword if it is appearing after the
        # refs field (i.e. if the current command length is 2)
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
