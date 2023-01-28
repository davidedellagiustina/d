# Mouse class

class Mouse(object):

	# Variables

	x_old, y_old = None, None

	# Function that gets the mouse movement (when left button is clicked) and draws on the widget which causes the event to happen

	@staticmethod
	def left_clicked_motion(event):
		if Mouse.x_old is not None and Mouse.y_old is not None:
			event.widget.create_oval(event.x - 10, event.y - 10, event.x + 10, event.y + 10, width = 1, fill = "#000")
			event.widget.create_line(Mouse.x_old, Mouse.y_old, event.x, event.y, width = 20)
		Mouse.x_old, Mouse.y_old = event.x, event.y

	# Function that resets the x and y values when the mouse left button is released

	@staticmethod
	def left_button_released(event):
		Mouse.x_old, Mouse.y_old = None, None