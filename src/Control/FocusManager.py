

class FocusManager:
    def __init__(self):
        self.focused = None
        self.state = None
        self.state_locked = False

    def get_focused(self):
        return self.focused

    def is_focused(self, caller):
        return self.focused == caller

    def lock_focus(self):
        self.state_locked = True

    def unlock_focus(self):
        self.state_locked = False

    def ask_for_focus(self, caller):
        if self.is_focused(caller):
            return True
        if not self.state_locked:
            self.focused = caller
            return True
        return False

    def release_focus(self):
        if not self.state_locked:
            self.focused = None
