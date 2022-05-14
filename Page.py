

class Position:
	def __init__(self,x,y):
		self.isEpmty = True
		self.position = [float(x),float(y)]


class SinglePage:
	
	def __init__(self,cardWidth,cardHeight):
		self.countOfFreePositions = 0
		self.positions = [
							Position(0,0),Position(float(cardWidth),0),Position(float(cardWidth)*2,0),
							Position(0,float(cardHeight)),Position(float(cardWidth),float(cardHeight)),Position(float(cardWidth)*2,float(cardHeight)),
							Position(0,float(cardHeight)*2),Position(float(cardWidth),float(cardHeight)*2),Position(float(cardWidth)*2,float(cardHeight)*2)
						 ]

	def isPageFull(self):
		for pos in self.positions:
			if pos.isEpmty == True:
				self.countOfFreePositions += 1
		if self.countOfFreePositions	== 0:
			return True
		else:
			self.countOfFreePositions = 0
			return False

	def getLastFreePos(self):
		for pos in self.positions:
			if pos.isEpmty == True:
				pos.isEpmty = False
				return pos.position