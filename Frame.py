

class Frame:
	def __init__(self,frameWidth,frameHeight):
		self.leftBorder = 0
		self.rightBorder = frameWidth
		self.upBorder = 0
		self.downBorder = frameHeight

		self.frameWidth = frameWidth
		self.frameHeight = frameHeight

	def moveFrame(self,direction):
		if direction == "right":
			self.leftBorder += self.frameWidth
			self.rightBorder += self.frameWidth
		if direction == "down":
			self.upBorder += self.frameHeight
			self.downBorder += self.frameHeight
		if direction == "beginColumn":
			self.leftBorder = 0
			self.rightBorder = self.frameWidth
		if direction == "endColumn":
			self.leftBorder = self.frameWidth * 10
			self.rightBorder = self.frameWidth * 10
	def show(self):
		print("Left = " + str(self.leftBorder) + "\tRight = " + str(self.rightBorder) + "\tUp = " + str(self.upBorder) + "\tDown = " + str(self.downBorder))
