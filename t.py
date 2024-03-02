import tkinter as tk

root = tk.Tk()

label1 = tk.Label(root, text="Label 1")
label1.grid(row=0, column=0, sticky="nsew")

label2 = tk.Label(root, text="Label 2")
label2.grid(row=1, column=0, sticky="nsew")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=3)

root.mainloop()