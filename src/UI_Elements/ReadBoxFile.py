import tkinter as tk
from functools import partial
from src.UI_Elements.util import in_range
from enum import Enum, auto
#from src.UI_Elements.InvisibleWindow import Overlay

class Sides(Enum):
    TOP = auto()
    BOT = auto()
    LEFT = auto()
    RIGHT = auto()
    TOP_MID = auto()
    BOT_MID = auto()
    LEFT_MID = auto()
    RIGHT_MID = auto()
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOT_RIGHT = auto()
    BOT_LEFT = auto()
    OUTSIDE = auto()
    INSIDE = auto()

side_cursor_dic = {
    Sides.BOT: '',
    Sides.LEFT:'',
    Sides.RIGHT: '',
    Sides.TOP: '',
    Sides.TOP_MID: 'size_ns',
    Sides.BOT_MID: 'size_ns',
    Sides.LEFT_MID: 'size_we',
    Sides.RIGHT_MID: 'size_we',
    Sides.TOP_LEFT: 'hand1',
    Sides.TOP_RIGHT: 'size_ne_sw',
    Sides.BOT_RIGHT: 'size_nw_se',
    Sides.BOT_LEFT: 'size_ne_sw',
    Sides.OUTSIDE: '',
    Sides.INSIDE: ''
}


class ReadBox:
    def __init__(self, id):
        self.x1 = 100
        self.y1 = 100
        self.x2 = 200
        self.y2 = 200
        self.bd_color = 'red'
        self.fill = 'white'
        self.bd_width = 10
        self.name = None
        self.read_list = None
        self.id = id
        self.focus_side = None

    def draw(self, canvas):
        focus_color = "green"
        if canvas.focus_manager.is_focused(self):
            outline_color = focus_color
        else:
            outline_color = self.bd_color
        rec = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                      fill=self.fill, outline=outline_color, width=self.bd_width)
        canvas.tag_bind(rec, "<Enter>", partial(self.on_enter, canvas))
        canvas.tag_bind(rec, "<Leave>", partial(self.on_leave, canvas))
        canvas.tag_bind(rec, "<ButtonPress-1>", self.on_press)
        canvas.tag_bind(rec, "<B1-Motion>", self.on_drag)
        canvas.tag_bind(rec, "<ButtonRelease-1>", self.on_release)

    def on_enter(self, *args):
        # https: // stackoverflow.com / questions / 54605404 / tkinter - how - to - change - cursor - over - canvas - items
        # https://tkdocs.com/shipman/cursors.html
        # https://www.tcl.tk/man/tcl8.6/TkCmd/cursors.htm
        canvas = args[0]
        event = args[1]
        if canvas.focus_manager.ask_for_focus(self):
            canvas.config(cursor=side_cursor_dic[self.get_mouse_side(event)])

    def on_leave(self, *args):
        canvas = args[0]
        event = args[1]
        if canvas.focus_manager.is_focused(self):
            canvas.config(cursor="")
            canvas.focus_manager.release_focus()
        print("leave", args)

    def on_press(self, event):
        print("press")
        self.focus_side = self.get_mouse_side(event)
        pass

    def on_drag(self, event):
        print("drag")
        side = self.focus_side
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        print(side, width, height)
        if side == Sides.TOP_MID:
            self.y1 = event.y
        elif side == Sides.BOT_MID:
            self.y2 = event.y
        elif side == Sides.RIGHT_MID:
            self.x2 = event.x
        elif side == Sides.LEFT_MID:
            self.x1 = event.x
        elif side == Sides.TOP_LEFT:
            self.x1 = event.x
            self.y1 = event.y
            self.x2 = self.x1 + width
            self.y2 = self.y1 + height
        elif side == Sides.TOP_RIGHT:
            self.x2 = event.x
            self.y1 = event.y
        elif side == Sides.BOT_RIGHT:
            self.x2 = event.x
            self.y2 = event.y
        elif side == Sides.BOT_LEFT:
            self.x1 = event.x
            self.y2 = event.y

    def on_release(self, event):
        self.focus_side = None
        print("release")
        pass

    def object_to_dic(self):
        dic = {}
        for attribute in vars(self):
            print(attribute)
            dic[str(attribute)] = self.__getattribute__(attribute)
        return dic

    def dic_to_object(self, dic):
        for attribute in vars(self):
            for key, value in dic.items():
                if str(attribute) == key:
                    self.__setattr__(attribute, value)

    def get_mouse_side(self, event):
        side_margin = 20
        middle_margin = 10
        mouse_x = event.x
        mouse_y = event.y
        top, bot, left, right, mid = [False]*5
        if mouse_y < self.y1 or mouse_y > self.y2 or mouse_x < self.x1 or mouse_x > self.x2:
            return Sides.OUTSIDE
        if self.y1 + side_margin < mouse_y < self.y2 - side_margin\
                and self.x1 + side_margin < mouse_x < self.x2 - side_margin:
            return Sides.INSIDE
        if self.x1 <= mouse_x <= self.x1 + side_margin:
            left = True
        elif self.x2-side_margin <= mouse_x <= self.x2:
            right = True
        if self.y1 <= mouse_y <= self.y1 + side_margin:
            top = True
        elif self.y2-side_margin <= mouse_y <= self.y2:
            bot = True
        if (top or bot) and not (left or right):
            horizontal_middle = self.x1 + ((self.x2-self.x1)/2.0)
            print(horizontal_middle, mouse_x)
            if abs(mouse_x - horizontal_middle) <= middle_margin:
                mid = True
        elif (left or right) and not (top or bot):
            vertical_middle = self.y1 + ((self.y2-self.y1)/2.0)
            if abs(mouse_y - vertical_middle) <= middle_margin:
                mid = True
        if top and mid:
            return Sides.TOP_MID
        if top and left:
            return Sides.TOP_LEFT
        if top and right:
            return Sides.TOP_RIGHT
        if top:
            return Sides.TOP
        if bot and mid:
            return Sides.BOT_MID
        if bot and left:
            return Sides.BOT_LEFT
        if bot and right:
            return Sides.BOT_RIGHT
        if bot:
            return Sides.BOT
        if left and mid:
            return Sides.LEFT_MID
        if left:
            return Sides.LEFT
        if right and mid:
            return Sides.RIGHT_MID
        if right:
            return Sides.RIGHT

