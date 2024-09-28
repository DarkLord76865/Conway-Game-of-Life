import os
import sys
import tkinter as tk


def update_gui():
	global kocke
	global kocke_gui
	global horizontal_move, vertical_move
	global field_sizes, current_field
	for i in range(field_sizes[current_field][1]):
		for j in range(field_sizes[current_field][0]):
			if (i + vertical_move, j + horizontal_move) in kocke:
				cnv.itemconfig(kocke_gui[i][j], fill="#ffffff")
			else:
				cnv.itemconfig(kocke_gui[i][j], fill="#000000")

def calc_gen():
	global kocke
	kocke_temp = set()
	crni_kand = set()
	for i in kocke:
		num_alive = 0
		for x in range(-1, 2):
			for y in range(-1, 2):
				if x != 0 or y != 0:
					if (i[0] + x, i[1] + y) in kocke:
						num_alive += 1
					else:
						crni_kand.add((i[0] + x, i[1] + y))
		if 2 <= num_alive <= 3:
			kocke_temp.add(i)
	while len(crni_kand) != 0:
		if crni_kand.count(crni_kand[0]) == 3:
			kocke_temp.add(crni_kand[0])
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
	global sim_speed
	if curr_num == sim_num:
		if calc_gen():
			root.after(int(round(sim_speed, 0)), lambda send_num=curr_num: auto_sim(send_num))
		else:
			stop_sim_click()

def mis_listen(event=None):
	global kocke
	global kocke_gui
	global started
	global horizontal_move, vertical_move
	global field_sizes, current_field
	if not started:
		if event.x % (field_sizes[current_field][2] + 1) <= (field_sizes[current_field][2] - 1) and (event.y - 1) % (field_sizes[current_field][2] + 1) <= (field_sizes[current_field][2] - 1):
			if ((event.y - 1) // (field_sizes[current_field][2] + 1) + vertical_move, event.x // (field_sizes[current_field][2] + 1) + horizontal_move) in kocke:
				cnv.itemconfig(kocke_gui[(event.y - 1) // (field_sizes[current_field][2] + 1)][event.x // (field_sizes[current_field][2] + 1)], fill="#000000")
				kocke.remove(((event.y - 1) // (field_sizes[current_field][2] + 1) + vertical_move, event.x // (field_sizes[current_field][2] + 1) + horizontal_move))
			else:
				cnv.itemconfig(kocke_gui[(event.y - 1) // (field_sizes[current_field][2] + 1)][event.x // (field_sizes[current_field][2] + 1)], fill="#ffffff")
				kocke.add(((event.y - 1) // (field_sizes[current_field][2] + 1) + vertical_move, event.x // (field_sizes[current_field][2] + 1) + horizontal_move))
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

def change_sim_speed(faster):
	global sim_speed
	if faster:
		sim_speed /= 2
	else:
		sim_speed *= 2

def change_zoom(out):
	global current_field
	old = current_field
	if out:
		if current_field != 2:
			current_field += 1
	else:
		if current_field != 0:
			current_field -= 1
	draw_current_zoom(old)


class App:
	def __init__(self):
		field_sizes = ((18, 11, 51), (36, 22, 25), (72, 44, 12))  # nx, ny, width
		current_field = 1

		sim_speed = 250

		self.cells = set()
		self.tiles = list()
		self.vertical_lines = list()
		self.horizontal_lines = list()
		self.tile_size = 25

		init_width = 935
		init_height = 652

		self.root = tk.Tk()
		self.root.minsize(init_width, init_height)
		self.root.geometry(f"{init_width}x{init_height}"
		                   f"+{self.root.winfo_screenwidth() // 2 - init_width // 2}"
		                   f"+{self.root.winfo_screenheight() // 2 - init_height // 2}")
		self.root.title("Conway's Game of Life")
		self.root.config(background="#ffffff")
		self.root.iconbitmap(self.resource_path("resources/cgol-icon.ico"))

		horizontal_move = 0
		vertical_move = 0
		self.root.bind("<KeyPress-Left>", lambda event: arrow_click(event, "press"))
		self.root.bind("<KeyPress-Right>", lambda event: arrow_click(event, "press"))
		self.root.bind("<KeyPress-Up>", lambda event: arrow_click(event, "press"))
		self.root.bind("<KeyPress-Down>", lambda event: arrow_click(event, "press"))
		self.root.bind("<KeyRelease-Left>", lambda event: arrow_click(event, "release"))
		self.root.bind("<KeyRelease-Right>", lambda event: arrow_click(event, "release"))
		self.root.bind("<KeyRelease-Up>", lambda event: arrow_click(event, "release"))
		self.root.bind("<KeyRelease-Down>", lambda event: arrow_click(event, "release"))
		keys_pressed = [False, False, False, False]  # left, right, up, down

		self.toolbar = tk.Frame(self.root, background="#ffffff", highlightthickness=0, width=init_width, height=60)
		self.toolbar.place(relwidth=1, relheight=50/init_height, relx=0, rely=0)

		self.title_lbl = tk.Label(self.toolbar, anchor="center", text="Conway's Game of Life", font="Helvetica 26 italic",
		                          background="#ffffff", foreground="#000000", highlightthickness=0)
		self.title_lbl.place(relx=0, rely=0, relwidth=400/init_width, relheight=1)

		self.stats = tk.Frame(self.toolbar, background="#808080", highlightthickness=0)
		self.stats.place(relx=400/init_width, rely=0, relwidth=135/init_width, relheight=1)

		self.stats_txt = tk.Label(self.stats, anchor="center", text="CELLS", font="Helvetica 11 bold",
		                          foreground="#74e66a", background="#808080", highlightthickness=0)
		self.stats_txt.place(relx=0, rely=0, relwidth=1, relheight=0.5)
		self.stats_num = tk.Label(self.stats, anchor="center", text="0", font="Helvetica 20 bold",
		                          foreground="#ffffff", background="#808080", highlightthickness=0)
		self.stats_num.place(relx=0, rely=0.42, relwidth=1, relheight=0.5)

		self.canvas = tk.Canvas(self.root, highlightthickness=0, background="#000000")
		self.canvas.place(relx=0, rely=50/init_height, relwidth=1, relheight=(init_height - 50)/init_height)
		self.canvas.bind("<MouseWheel>", lambda event: print(event))  # +120/-120 .delta

		plus_img = tk.PhotoImage(file=self.resource_path("resources/plus-sign.png"))
		minus_img = tk.PhotoImage(file=self.resource_path("resources/minus-sign.png"))
		speed_up_btn = tk.Button(self.root, image=plus_img,
		                      borderwidth=0, highlightthickness=0,
		                      background="#ffffff", activebackground="#ffffff")
		speed_up_btn.place(x=895, y=0, height=40, width=40)
		slow_down_btn = tk.Button(self.root, image=minus_img,
		                       anchor="center", borderwidth=0, highlightthickness=0,
		                       background="#ffffff", activebackground="#ffffff")
		slow_down_btn.place(x=895, y=40, height=40, width=40)

		speed_up_btn.bind("<ButtonRelease-1>", lambda event: change_sim_speed(True))
		slow_down_btn.bind("<ButtonRelease-1>", lambda event: change_sim_speed(False))

		#zoom_in_img = tk.PhotoImage(file=self.resource_path("resources/zoom-in.png"))
		#zoom_out_img = tk.PhotoImage(file=self.resource_path("resources/zoom-out.png"))
		#zoom_in_btn = tk.Button(self.root, image=zoom_in_img,
		#                     borderwidth=0, highlightthickness=0,
		#                     background="#ffffff", activebackground="#ffffff")
		#zoom_in_btn.place(x=535, y=0, height=40, width=40)
		#zoom_out_btn = tk.Button(self.root, image=zoom_out_img,
		#                      anchor="center", borderwidth=0, highlightthickness=0,
		#                      background="#ffffff", activebackground="#ffffff")
		#zoom_out_btn.place(x=535, y=40, height=40, width=40)

		#zoom_in_btn.bind("<ButtonRelease-1>", lambda event: change_zoom(False))
		#zoom_out_btn.bind("<ButtonRelease-1>", lambda event: change_zoom(True))

		start_sim_bt = tk.Button(self.root, anchor="center", text="START SIMULATION", borderwidth=0, font="Helvetica 11 bold",
		                      background="#ffffff", activebackground="#ffffff", foreground="#000000",
		                      activeforeground="#000000")
		start_sim_bt.place(x=575, y=0, height=40, width=160)
		start_sim_bt.bind("<ButtonRelease-1>", start_sim_click)

		stop_sim_bt = tk.Button(self.root, anchor="center", text="STOP SIMULATION", borderwidth=0, font="Helvetica 11 bold",
		                     background="#ffffff", activebackground="#ffffff", foreground="#808080",
		                     activeforeground="#808080")
		stop_sim_bt.place(x=735, y=0, height=40, width=160)
		stop_sim_bt.bind("<ButtonRelease-1>", stop_sim_click)

		next_gen_bt = tk.Button(self.root, anchor="center", text="NEXT GENERATION", borderwidth=0, font="Helvetica 11 bold",
		                     background="#ffffff", activebackground="#ffffff", foreground="#000000",
		                     activeforeground="#000000")
		next_gen_bt.place(x=575, y=40, height=40, width=160)
		next_gen_bt.bind("<ButtonRelease-1>", next_gen_click)

		rst_bt = tk.Button(self.root, anchor="center", text="RESET", borderwidth=0, font="Helvetica 11 bold",
		                background="#ffffff", activebackground="#ffffff", foreground="red", activeforeground="red")
		rst_bt.place(x=735, y=40, height=40, width=160)
		rst_bt.bind("<ButtonRelease-1>", rst)

		#draw_current_zoom()

		started = False
		sim_num = 0

		self.root.mainloop()

	def draw_zoom(self):
		self.canvas.delete("all")
		self.tiles.clear()
		self.vertical_lines.clear()
		self.horizontal_lines.clear()

		# horizontal lines
		horizontal_loc = 0
		while horizontal_loc < self.canvas.winfo_height():
			self.horizontal_lines.append(self.canvas.create_line(0, horizontal_loc, self.canvas.winfo_width(), horizontal_loc, fill="#808080"))
			horizontal_loc += self.tile_size + 1
		self.horizontal_lines.append(self.canvas.create_line(0, horizontal_loc, self.canvas.winfo_width(), horizontal_loc, fill="#808080"))

		# vertical lines
		vertical_loc = 0
		while vertical_loc < self.canvas.winfo_width():
			self.vertical_lines.append(self.canvas.create_line(vertical_loc, 0, vertical_loc, self.canvas.winfo_height(), fill="#808080"))
			vertical_loc += self.tile_size + 1
		self.vertical_lines.append(self.canvas.create_line(vertical_loc, 0, vertical_loc, self.canvas.winfo_height(), fill="#808080"))

		for i in range(field_sizes[current_field][1]):
			red_gui = []
			for j in range(field_sizes[current_field][0]):
				red_gui.append(cnv.create_rectangle(j * (field_sizes[current_field][2] + 1),
				                                    i * (field_sizes[current_field][2] + 1) + 1,
				                                    j * (field_sizes[current_field][2] + 1) +
				                                    field_sizes[current_field][2],
				                                    i * (field_sizes[current_field][2] + 1) +
				                                    field_sizes[current_field][2] + 1, fill="#000000", width=0))
			kocke_gui.append(red_gui)

		if old_zoom is not None:
			horizontal_move += (field_sizes[old_zoom][0] - field_sizes[current_field][0]) // 2
			vertical_move += (field_sizes[old_zoom][1] - field_sizes[current_field][1]) // 2
			if old_zoom != current_field and old_zoom == 0:
				vertical_move += 1
		update_gui()

	@staticmethod
	def resource_path(relative_path):
		""" Get absolute path to resource, works for dev and for PyInstaller """
		try:
			# PyInstaller creates a temp folder and stores path in _MEIPASS
			base_path = sys._MEIPASS
		except AttributeError:
			base_path = os.path.abspath(".")
		return os.path.join(base_path, relative_path)


if __name__ == "__main__":
	App()
