import tkinter as tk

main_window = tk.Tk()


def check_hand_enter():
    canvas.config(cursor="hand1")


def check_hand_leave():
    canvas.config(cursor="")


canvas = tk.Canvas(width=200, height=200)
tag_name = "polygon"

canvas.create_polygon((25, 25), (25, 100), (125, 100), (125, 25), outline='black', fill="", tag=tag_name)

canvas.tag_bind(tag_name, "<Enter>", lambda event: check_hand_enter())
canvas.tag_bind(tag_name, "<Leave>", lambda event: check_hand_leave())

canvas.pack()
main_window.mainloop()