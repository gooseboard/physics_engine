class Actor:
	def __init__(self,x_pos, y_pos, h, w,  xv, yv, color, x_prev, y_prev):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.h = h
		self.w = w
		self.xv = xv
		self.yv = yv
		self.color = color
		self.y_prev = y_prev
		self.x_prev = x_prev


class Rectangle(Actor):
	def __init__(self, x_pos, y_pos, h, w,  xv, yv, color, x_prev, y_prev):
		Actor.__init__(self, x_pos, y_pos, h, w,  xv, yv, color, x_prev, y_prev)

