from tkinter import *
import os
import sys
try:
	import pyi_splash
	pyi_splash.close()
except ModuleNotFoundError:
	pass


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def update_gui():
	global kocke
	global kocke_gui
	global horizontal_move, vertical_move
	for i in range(22):
		for j in range(36):
			if (i + vertical_move, j + horizontal_move) in kocke:
				cnv.itemconfig(kocke_gui[i][j], fill="#ffffff")
			else:
				cnv.itemconfig(kocke_gui[i][j], fill="#000000")

def calc_gen():
	global kocke
	kocke_temp = []
	crni_kand = []
	for i in kocke:
		num_alive = 0
		for x in range(-1, 2):
			for y in range(-1, 2):
				if not (x == 0 and y == 0):
					if (i[0] + x, i[1] + y) in kocke:
						num_alive += 1
					else:
						crni_kand.append((i[0] + x, i[1] + y))
		if 2 <= num_alive <= 3:
			kocke_temp.append(i)
	while len(crni_kand) != 0:
		if crni_kand.count(crni_kand[0]) == 3:
			kocke_temp.append(crni_kand[0])
		crni_kand = [x for x in crni_kand if x != crni_kand[0]]
	if kocke != kocke_temp:
		kocke = kocke_temp
		result = True
	else:
		result = False
	update_gui()
	updt_br_cell()
	return result

def auto_sim(curr_num):
	global sim_num
	if curr_num == sim_num:
		if calc_gen():
			root.after(250, lambda send_num=curr_num: auto_sim(send_num))
		else:
			stop_sim_click()

def mis_listen(event=None):
	global kocke
	global kocke_gui
	global started
	global horizontal_move, vertical_move
	if not started:
		if event.x % 26 <= 24 and (event.y - 1) % 26 <= 24:
			if ((event.y - 1) // 26 + vertical_move, event.x // 26 + horizontal_move) in kocke:
				cnv.itemconfig(kocke_gui[(event.y - 1) // 26][event.x // 26], fill="#000000")
				kocke.remove(((event.y - 1) // 26 + vertical_move, event.x // 26 + horizontal_move))
			else:
				cnv.itemconfig(kocke_gui[(event.y - 1) // 26][event.x // 26], fill="#ffffff")
				kocke.append(((event.y - 1) // 26 + vertical_move, event.x // 26 + horizontal_move))
		updt_br_cell()

def rst(event=None):
	global started
	global kocke
	global sim_num
	started = False
	sim_num += 1
	kocke.clear()
	update_gui()
	updt_br_cell()
	start_sim_bt.config(foreground="#000000", activeforeground="#000000")
	next_gen_bt.config(foreground="#000000", activeforeground="#000000")
	stop_sim_bt.config(foreground="#808080", activeforeground="#808080")

def start_sim_click(event=None):
	global started
	global sim_num
	if not started:
		started = True
		start_sim_bt.config(foreground="#808080", activeforeground="#808080")
		next_gen_bt.config(foreground="#808080", activeforeground="#808080")
		stop_sim_bt.config(foreground="#000000", activeforeground="#000000")
		auto_sim(sim_num)

def stop_sim_click(event=None):
	global started
	global sim_num
	if started:
		started = False
		sim_num += 1
		start_sim_bt.config(foreground="#000000", activeforeground="#000000")
		next_gen_bt.config(foreground="#000000", activeforeground="#000000")
		stop_sim_bt.config(foreground="#808080", activeforeground="#808080")

def next_gen_click(event=None):
	global started
	if not started:
		calc_gen()

def updt_br_cell():
	global kocke
	alive_info.config(text=str(len(kocke)))

def arrow_click(event, state):
	global horizontal_move, vertical_move
	global keys_pressed

	match event.keysym:
		case "Left":
			if state == "press":
				keys_pressed[0] = True
			else:
				keys_pressed[0] = False
		case "Right":
			if state == "press":
				keys_pressed[1] = True
			else:
				keys_pressed[1] = False
		case "Up":
			if state == "press":
				keys_pressed[2] = True
			else:
				keys_pressed[2] = False
		case "Down":
			if state == "press":
				keys_pressed[3] = True
			else:
				keys_pressed[3] = False

	horizontal_move += -int(keys_pressed[0]) + int(keys_pressed[1])
	vertical_move += -int(keys_pressed[2]) + int(keys_pressed[3])
	update_gui()


if __name__ == "__main__":

	root = Tk()
	width = 935
	height = 650
	root.geometry(f"{width}x{height}+{root.winfo_screenwidth() // 2 - width // 2}+{root.winfo_screenheight() // 2 - height // 2}")
	root.resizable(False, False)
	root.title("Conway's Game of Life")
	root.iconbitmap(resource_path("cgol.ico"))

	horizontal_move = 0
	vertical_move = 0
	root.bind("<KeyPress-Left>", lambda event: arrow_click(event, "press"))
	root.bind("<KeyPress-Right>", lambda event: arrow_click(event, "press"))
	root.bind("<KeyPress-Up>", lambda event: arrow_click(event, "press"))
	root.bind("<KeyPress-Down>", lambda event: arrow_click(event, "press"))
	root.bind("<KeyRelease-Left>", lambda event: arrow_click(event, "release"))
	root.bind("<KeyRelease-Right>", lambda event: arrow_click(event, "release"))
	root.bind("<KeyRelease-Up>", lambda event: arrow_click(event, "release"))
	root.bind("<KeyRelease-Down>", lambda event: arrow_click(event, "release"))
	keys_pressed = [False, False, False, False]  # left, right, up, down

	naslov = Label(root, anchor="center", text="Conway's Game of Life", font="Helvetica 26 italic", background="#ffffff", foreground="#000000", highlightthickness=0)
	naslov.place(x=0, y=0, height=78, width=400)

	start_sim_bt = Button(root, anchor="center", text="START SIMULATION", borderwidth=0, font="Helvetica 11 bold", background="#ffffff", activebackground="#ffffff", foreground="#000000", activeforeground="#000000")
	start_sim_bt.place(x=535, y=0, height=39, width=200)
	start_sim_bt.bind("<ButtonRelease-1>", start_sim_click)

	stop_sim_bt = Button(root, anchor="center", text="STOP SIMULATION", borderwidth=0, font="Helvetica 11 bold", background="#ffffff", activebackground="#ffffff", foreground="#808080", activeforeground="#808080")
	stop_sim_bt.place(x=735, y=0, height=39, width=200)
	stop_sim_bt.bind("<ButtonRelease-1>", stop_sim_click)

	next_gen_bt = Button(root, anchor="center", text="NEXT GENERATION", borderwidth=0, font="Helvetica 11 bold", background="#ffffff", activebackground="#ffffff", foreground="#000000", activeforeground="#000000")
	next_gen_bt.place(x=535, y=39, height=39, width=200)
	next_gen_bt.bind("<ButtonRelease-1>", next_gen_click)

	rst_bt = Button(root, anchor="center", text="RESET", borderwidth=0, font="Helvetica 11 bold", background="#ffffff", activebackground="#ffffff", foreground="red", activeforeground="red")
	rst_bt.place(x=735, y=39, height=39, width=200)
	rst_bt.bind("<ButtonRelease-1>", rst)

	alive_lbl = Label(root, background="#808080", highlightthickness=0)
	alive_lbl.place(x=400, y=0, height=78, width=135)
	alive_al_txt = Label(root, anchor="center", text="CELLS", font="Helvetica 11 bold", foreground="#74e66a", background="#808080", highlightthickness=0)
	alive_al_txt.place(x=400, y=9, width=135, height=15)
	alive_info = Label(root, anchor="center", text="0", font="Helvetica 20 bold", foreground="#ffffff", background="#808080", highlightthickness=0)
	alive_info.place(x=400, y=33, width=135, height=25)

	arrow_help = Label(root, anchor="center", text="Use arrow keys to move", font="Helvetica 8 italic", background="#808080", foreground="#ffffff", highlightthickness=0)
	arrow_help.place(x=400, y=66, height=12, width=135)

	cnv = Canvas(root, width=width, height=572, highlightthickness=0)
	cnv.place(x=0, y=78)
	cnv.bind("<ButtonRelease-1>", mis_listen)

	for i in range(0, 572, 26):
		cnv.create_line(0, i, width, i, fill="#808080", width=1)
	for i in range(25, 935, 26):
		cnv.create_line(i, 0, i, 572, fill="#808080", width=1)

	kocke = []
	kocke_gui = []
	for i in range(22):
		red_gui = []
		for j in range(36):
			red_gui.append(cnv.create_rectangle(j * 26, i * 26 + 1, j * 26 + 25, i * 26 + 25 + 1, fill="#000000", width=0))
		kocke_gui.append(red_gui)
	del red_gui

	started = False
	sim_num = 0

	root.mainloop()
