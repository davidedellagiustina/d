import time
import numpy as np
import pygubu
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from bin.modules.ann_view import AnnView
from bin.modules.console import Console
from bin.modules.img_preprc import Image
from bin.modules.mouse import Mouse
from bin.modules.ann import Ann
from bin.neural_network.network import NeuralNetwork

# Application class

class Application(object):

	# Constants

	TITLE = "Handwritten Digits Classifier"
	ICON = "res/images/favicon.ico"
	GEOMETRY = (1018, 577)
	GUI = "res/graphics/main.ui"

	# Settings

	ANN = "ann_2h12050_9702"

	# Variables

	preprc_pics = {}

	# Constructor - creates and builds the main window

	def __init__(self):
		# Create window
		self.window = tk.Tk()
		# Set window geometry
		self.window.update_idletasks()
		frm_width = self.window.winfo_rootx() - self.window.winfo_x()
		ttlbar_height = self.window.winfo_rooty() - self.window.winfo_y()
		x = int((self.window.winfo_screenwidth() / 2) - ((self.GEOMETRY[0] + 2 * frm_width) / 2))
		y = int((self.window.winfo_screenheight() / 2) - ((self.GEOMETRY[1] + frm_width + ttlbar_height) / 2))
		self.window.geometry("%sx%s+%s+%s" % (self.GEOMETRY[0], self.GEOMETRY[1], x, y))
		# Set window title and icon
		self.window.title(self.TITLE)
		self.window.wm_iconbitmap(self.ICON)
		self.window.deiconify()
		self.window.resizable(False, False)
		# Build window graphics
		builder = pygubu.Builder()
		builder.add_from_file(self.GUI)
		self.mainframe = builder.get_object("mainframe", self.window)
		self.window.config(menu = builder.get_object("menu", self.window))
		builder.connect_callbacks(self)
		# Mapping canvases for preprocessing stages
		self.stage_1 = builder.get_object("stage_1", self.window)
		self.stage_2 = builder.get_object("stage_2", self.window)
		self.stage_3 = builder.get_object("stage_3", self.window)
		self.stage_4 = builder.get_object("stage_4", self.window)
		self.stage_5 = builder.get_object("stage_5", self.window)
		# Initializing console
		self.console = Console(self.window, builder.get_object("console", self.window), builder.get_object("scrollbar_console", self.window))
		# Mouse input (for drawing area)
		self.drawing_area = builder.get_object("drawing_area", self.window)
		self.drawing_area.bind("<B1-Motion>", Mouse.left_clicked_motion)
		self.drawing_area.bind("<ButtonRelease-1>", Mouse.left_button_released)
		# Keyboard shoortcuts
		self.window.bind("<Control-c>", self.clear)
		self.window.bind("<Control-p>", self.process)
		self.window.bind("<Control-q>", self.quit)
		# ANN
		self.ann = Ann.unpickle("res/neural_network/" + self.ANN + ".pkl")
		# ANN output area
		self.ann_view = AnnView(self.window, builder.get_object("ann_view", self.window))

	# Function that does the processing of the image

	def process(self, event = None):
		# Capture image
		self.console.log("Image processing started ...")
		self.console.log("Capturing image ...")
		"""
		# OLD CODE TO GET CANVAS CONTENT: DOESN'T WORK WITH HiDPI DISPLAYS
		x1 = self.window.winfo_rootx() + self.drawing_area.winfo_x() + 10 + 1
		y1 = self.window.winfo_rooty() + self.drawing_area.winfo_y() + 5 + 1
		x2 = x1 + self.drawing_area.winfo_width() - 2
		y2 = y1 + self.drawing_area.winfo_height() - 2
		self.img = Image(x1, y1, x2, y2)
		"""
		self.img = Image(self.drawing_area)
		# Grayscale
		self.console.log("Grayscaling ...")
		self.img.grayscale()
		self.preprc_pics[0] = self.img.get((292, 292))
		self.stage_1.create_image(1, 1, anchor = tk.NW, image = self.preprc_pics[0])
		# If image is not empty
		self.img.invert()
		sum = np.sum(self.img.img)
		self.img.invert()
		if sum != 0:
			# Colour inversion
			self.console.log("Inverting ...")
			self.img.invert()
			self.preprc_pics[1] = self.img.get((140, 140))
			self.stage_2.create_image(1, 1, anchor = tk.NW, image = self.preprc_pics[1])
			# Cutting
			self.console.log("Cutting ...")
			self.img.cut()
			self.preprc_pics[2] = self.img.get((140, 140))
			self.stage_3.create_image(1, 1, anchor = tk.NW, image = self.preprc_pics[2])
			# Resizing
			self.console.log("Resizing ...")
			self.img.resize()
			self.preprc_pics[3] = self.img.get((140, 140))
			self.stage_4.create_image(1, 1, anchor = tk.NW, image = self.preprc_pics[3])
			# Centering
			self.console.log("Centering ...")
			self.img.center_of_mass()
			self.preprc_pics[4] = self.img.get((140, 140))
			self.stage_5.create_image(1, 1, anchor = tk.NW, image = self.preprc_pics[4])
			# Classifying
			self.classify()
			# Log
			self.console.log("Done.")
		# If image is empty
		else:
			self.img.img = np.zeros((28, 28))
			self.console.log("Error! Image was empty.")
		self.window.after(1200, self.console.ready)

	# Function that calls the neural network to classify the digit

	def classify(self):
		output = self.ann.feedforward(self.img.ready())
		digit = np.argmax(output)
		self.console.log("Elaborating digit ...")
		self.ann_view.echo(output.reshape(10), digit)

	# Function that clears the drawing area

	def clear(self, event = None):
		# Clear drawing area
		self.drawing_area.delete("all")
		# Clear all preprocessing stages
		self.stage_1.delete("all")
		self.stage_2.delete("all")
		self.stage_3.delete("all")
		self.stage_4.delete("all")
		self.stage_5.delete("all")
		# Delete references to preprocessing stages
		self.preprc_pics = {}
		# Delete AnnView
		self.ann_view.clear()
		# Log
		self.console.log("Drawing area was cleared.")

	# Function that runs the application

	def run(self):
		self.window.mainloop()

	# Function that asks the user whether he is sure to quit application, then destroys the main window

	def quit(self, event = None):
		self.console.log("Quitting application ...")
		answer = messagebox.askokcancel("Quit", "Are you sure you want to quit?")
		if answer:
			self.console.log("Done.")
			self.window.destroy()
		else:
			self.console.log("Aborted.")

# Application instantiation and start

if __name__ == "__main__":
	app = Application()
	app.run()