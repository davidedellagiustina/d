import tkinter as tk
from tkinter import *
from tkinter.ttk import *

# AnnView class

class AnnView(object):

	# Constructor

	def __init__(self, window, widget):
		self.window = window
		self.ann_view = widget
		self.ann_view.tag_configure("FOUND", foreground="#F44336")

	# Function that clears the text inside the AnnView

	def clear(self):
		self.ann_view.config(state = "normal")
		self.ann_view.delete("0.0", "end")
		self.ann_view.see(tk.END)
		self.ann_view.config(state = "disabled")

	# Function that prints the passed result in the AnnElaboration window

	def echo(self, output, digit):
		self.ann_view.config(state = "normal")
		self.ann_view.delete("0.0", "end")
		self.ann_view.insert(tk.END, "[ ")
		i = 1
		for o in output:
			out = format(round(o, 3)*100, '.1f').zfill(5)
			cs = self.ann_view.index(tk.INSERT)
			self.ann_view.insert(tk.END, ("  " if i != 1 else "") + str(i-1) + ": " + out + " %" + ("\n" if i % 3 == 0 else (", " if i != 10 else "")))
			if i-1 == digit: self.ann_view.tag_add("FOUND", cs, ("end-2c" if i % 3 == 0 else "end-3c"))
			i += 1
		self.ann_view.insert(tk.END, " ]\n\n")
		self.ann_view.insert(tk.END, "You wrote " + str(digit) + ".")
		self.ann_view.see(tk.END)
		self.ann_view.config(state = "disabled")