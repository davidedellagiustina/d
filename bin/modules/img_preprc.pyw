import numpy as np
from scipy import ndimage
import io, math
import PIL
from PIL import Image, ImageGrab, ImageTk

# Image class

class Image(object):

	"""
	OLD CONSTRUCTOR: DOESN'T WORK WITH HiDPI DISPLAYS
	# Constructor - grabs the image at the given coordinates
	def __init__(self, x1, y1, x2, y2):
		img = ImageGrab.grab((x1, y1, x2, y2))
		self.img = np.array(img)
	"""
	
	# Constructor - grabs the image inside the canvas
	
	def __init__(self, canvas):
		eps = canvas.postscript(colormode='color')
		img = PIL.Image.open(io.BytesIO(eps.encode('utf-8')))
		self.img = np.array(img)

	# Function that transforms the image to b&w (grayscale)

	def grayscale(self):
		img = PIL.Image.fromarray(np.uint8(self.img))
		img = img.convert("L")
		self.img = np.array(img)

	# Function that inverts the image (from white writing on black background, to black writing on white background)

	def invert(self):
		self.img = np.array(list(map(lambda x: 255 - x, self.img)))

	# Function that cuts all the empty rows and columns at the edges

	def cut(self):
		# Remove all empty rows and columns at the edges - Top, left, bottom, right
		while np.sum(self.img[0]) == 0:
			self.img = self.img[1:]
		while np.sum(self.img[:,0]) == 0:
			self.img = np.delete(self.img, 0, 1)
		while np.sum(self.img[-1]) == 0:
			self.img = self.img[:-1]
		while np.sum(self.img[:,-1]) == 0:
			self.img = np.delete(self.img, -1, 1)

	# Function that resizes the image to fit in a 20x20 box, then adds black rows and columns at the edges to get a 28x28 pixel image

	def resize(self):
		# Calculate factor and resize to fit in a 20x20 box
		rows, cols = self.img.shape
		img = PIL.Image.fromarray(np.uint8(self.img))
		if rows > cols:
			factor = 20.0 / rows
			img = img.resize((int(round(cols * factor)), 20), resample = PIL.Image.LANCZOS)
		else:
			factor = 20.0 / cols
			img = img.resize((20, int(round(rows * factor))), resample = PIL.Image.LANCZOS)
		self.img = np.array(img)
		# Add black rows and columns at the edges to get a 28x28 pixel image
		rows, cols = self.img.shape
		cols_pad = (int(math.ceil((28 - cols) / 2.0)), int(math.floor((28 - cols) / 2.0)))
		rows_pad = (int(math.ceil((28 - rows) / 2.0)), int(math.floor((28 - rows) / 2.0)))
		self.img = np.lib.pad(self.img, (rows_pad, cols_pad), 'constant')

	# Function that flattens the image to just black or white

	def threshold(self):
		self.img = np.array([list(map(lambda x: 0 if x < 128 else 255, img_row)) for img_row in self.img])

	# Function that centers the image by computing its center of mass

	def center_of_mass(self):
		# Compute center of mass
		cy, cx = ndimage.measurements.center_of_mass(self.img)
		# Shift image
		rows, cols = self.img.shape
		shift_x = np.round(cols / 2.0 - cx).astype(int)
		shift_y = np.round(rows / 2.0 - cy).astype(int)
		self.img = np.roll(self.img, shift_x, axis = 1)
		self.img = np.roll(self.img, shift_y, axis = 0)

	# Function that returns a PIL.Image object

	def get(self, size):
		# Avoid stretching
		rows, cols = self.img.shape
		if not size[0]/size[1] == cols/rows:
			if rows > cols: m = rows
			else: m = cols
			cols_pad = (int(math.ceil((m - cols) / 2.0)), int(math.floor((m - cols) / 2.0)))
			rows_pad = (int(math.ceil((m - rows) / 2.0)), int(math.floor((m - rows) / 2.0)))
			self.img = np.lib.pad(self.img, (rows_pad, cols_pad), 'constant')
		# Return the resized PhotoImage
		return PIL.ImageTk.PhotoImage(PIL.Image.fromarray(np.uint8(self.img)).resize(size, resample = PIL.Image.NEAREST))

	# Function that makes the image ready to be processed by the neural network

	def ready(self):
		img = np.zeros((784, 1))
		i = 0
		for pixel in self.img.reshape(784, 1):
			img[i][0] = float(pixel[0]) / 255
			i += 1
		return img

	# Function that saves the image in the /tmp folder

	def save(self):
		img = PIL.Image.fromarray(np.uint8(self.img))
		img.save("tmp/img.png", dpi = (6000, 6000))