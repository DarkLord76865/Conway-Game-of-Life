import tkinter as tk

def drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    widget.configure(cursor="fleur")

def drag_motion(event):
    widget = event.widget
    dx = event.x - widget._drag_start_x
    dy = event.y - widget._drag_start_y
    widget.move("all_objects", dx, dy)
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def drag_stop(event):
    # Reset the cursor to the default arrow
    event.widget.config(cursor="")


root = tk.Tk()
root.resizable(False, False)
root.geometry(f'300x300+{root.winfo_screenwidth() // 2 - 150}+{root.winfo_screenheight() // 2 - 150}')

cnv = tk.Canvas(root, width=300, height=300)
rect = cnv.create_rectangle(50, 50, 250, 250, fill='blue', tags="all_objects")
cnv.pack()
cnv.bind('<Button-2>', drag_start)
cnv.bind('<B2-Motion>', drag_motion)
cnv.bind('<ButtonRelease-2>', drag_stop)

root.mainloop()
