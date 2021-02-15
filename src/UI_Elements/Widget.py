from functools import partial

class Widget:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.shape = None
        self.text = None
        self.command = None

        self.bind("<ButtonPress-3>", partial(print, 3))