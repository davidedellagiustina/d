import tkinter as tk
from tkinter import *
from tkinter.ttk import *

# Console class

class Console(object):

	# Constants

	CURSOR = "_"

	# Variables

	cursor_state = 0

	# Constructor

	def __init__(self, window, widget, scrollbar):
		self.window = window
		self.console = widget
		scrollbar.config(command = self.console.yview)
		self.console['yscrollcommand'] = scrollbar.set
		self.blink_cursor()
		self.window.after(1200, self.ready)

	# Function that controls the cursor blink

	def blink_cursor(self):
		self.console.config(state = "normal")
		#current_state = self.console.get("end-2c", "end-1c")
		#next_state = self.CONSOLE_CURSOR if current_state == " " else " "
		next_state = self.CURSOR if self.cursor_state == 0 else " "
		self.cursor_state = (self.cursor_state + 1) % 2
		self.console.delete("end-2c", "end-1c")
		self.console.insert(tk.END, next_state)
		self.console.config(state = "disabled")
		self.window.after(500, self.blink_cursor)

	# Function that prints the "Ready." message in the console window

	def ready(self):
		self.log("Ready.\nWaiting for commands ...")

	# Function that prints a text in the console window and appends a newline character

	def log(self, log):
		self.console.config(state = "normal")
		self.console.delete("end-2c", "end-1c")
		self.console.insert(tk.END, log + "\n" + self.CURSOR)
		self.console.see(tk.END)
		self.console.config(state = "disabled")