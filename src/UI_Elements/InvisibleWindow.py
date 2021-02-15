
import tkinter as tk
from functools import partial
from win32api import GetSystemMetrics
import pyautogui  # Do not remove: This makes other screen tools work correctly

from src.UI_Elements.ReadBoxManager import ReadBoxManager

def log(text, *args):
    print(text)

class Overlay(tk.Canvas):
    def __init__(self):
        screen_width = GetSystemMetrics(0)
        screen_height = GetSystemMetrics(1)
        tk.Canvas.__init__(self, bg='white', width=screen_width, height=screen_height)
        self.dense = False
        self.widgets = []
        self.make_on_top_and_transparent()
        self.read_box_manager = ReadBoxManager()
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Button-3>", self.switch_density)
        self.scroll_states = ["Transp", "Add", "Move", "Resize", "Delete"]
        self.scroll_state = 0
        self.sub_state = None
        self.state_lock = False
        self.focus_box = None
        self.bind_all('<MouseWheel>', self.on_scroll)
        self.draw()
        self.pack()
        self.mainloop()

    def make_on_top_and_transparent(self):
        self.master.overrideredirect(True)  # Removes window top bar
        self.master.geometry("+0+0")
        self.master.lift()
        self.master.wm_attributes("-topmost", True)
        # self.master.wm_attributes("-disabled", False)
        self.master.wm_attributes("-transparentcolor", "white")

    def add_buttons(self):
        button1 = tk.Button(self, text="Dense", command=self.switch_density, anchor='w')
        button1.configure(width=10, activebackground="#33B5E5", relief='flat')
        button1_window = self.create_window(10, 10, anchor='nw', window=button1)

        button2 = tk.Button(self, text="Quit", command=self.quit, anchor='w')
        button2.configure(width=10, activebackground="#33B5E5", relief='flat')
        button2_window = self.create_window(110, 10, anchor='nw', window=button2)

        button3 = tk.Button(self, text="draw", command=self.draw, anchor='w')
        button3.configure(width=10, activebackground="#33B5E5", relief='flat')
        button3_window = self.create_window(210, 10, anchor='nw', window=button3)

    def switch_density(self, *args):
        if not self.dense:
            self.master.attributes("-alpha", 0.3)
            self.configure(bg="gray")
        else:
            self.master.attributes("-alpha", 1)
            self.configure(bg="white")
        self.dense = not self.dense
        self.master.update_idletasks()

    def draw(self):
        self.delete("all")
        self.add_buttons()
        self.draw_scroll_state()
        self.read_box_manager.draw_all(self)
        self.create_rectangle(500, 500, 600, 600, fill="black", outline="red", width=20)
        self.after(100, self.draw)

    def on_press(self, event):
        log("on press")
        if self.scroll_states[self.scroll_state] == "Add" and not self.sub_state:
            self.add(event)

    def on_drag(self, event):
        log("on drag")
        if self.scroll_states[self.scroll_state] == "Add" and self.sub_state == "adding":
            self.resize(event)

    def on_release(self, event):
        log("on release")
        if self.scroll_states[self.scroll_state] == "Add" and self.sub_state == "adding":
            self.finalize_adding(event)

    def add(self, event):
        box = self.read_box_manager.create_new_read_box()
        box.x1 = event.x
        box.y1 = event.y
        box.x2 = event.x
        box.y2 = event.y
        self.sub_state = "adding"
        self.state_lock = True
        self.focus_box = box
        log("Adding")

    def resize(self, event):
        self.focus_box.x1 = event.x
        self.focus_box.y1 = event.y
        log("Resizing")

    def finalize_adding(self, event):
        self.focus_box.x1 = event.x
        self.focus_box.y1 = event.y
        self.sub_state = None
        self.focus_box = None
        self.state_lock = False
        log("Finalized")

    def on_scroll(self, *args):
        log("Scroll")
        if self.state_lock:
            return
        event = args[0]
        if event.delta < 0:
            self.scroll_state = (self.scroll_state + 1) % len(self.scroll_states)
        else:
            self.scroll_state = (self.scroll_state - 1) % len(self.scroll_states)

    def draw_scroll_state(self):
        self.create_rectangle(300, 20, 330, 50, fill="green")
        self.create_text(310, 30, text=self.scroll_states[self.scroll_state])


Overlay()

