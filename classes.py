class Actor:
	def __init__(self,x_pos, y_pos, h, w,  xv, yv, color):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.h = h
		self.w = w
		self.xv = xv
		self.yv = yv
		self.color = color
		


class Rectangle(Actor):
	def __init__(self, x_pos, y_pos, h, w,  xv, yv, color):
		Actor.__init__(self, x_pos, y_pos, h, w,  xv, yv, color)

